import pandas as pd

ja3 = pd.read_csv("dataset/ja3_all.csv", low_memory=False)

def flow_key(ip1, p1, ip2, p2):
    try:
        p1 = int(float(p1))
        p2 = int(float(p2))
    except:
        return None

    a = f"{ip1}:{p1}-{ip2}:{p2}"
    b = f"{ip2}:{p2}-{ip1}:{p1}"
    return min(a, b)

ja3["flow_id"] = ja3.apply(
    lambda r: flow_key(
        r["ip.src"], r["tcp.srcport"],
        r["ip.dst"], r["tcp.dstport"]
    ),
    axis=1
)

ja3 = ja3.dropna(subset=["flow_id"])
ja3 = ja3.sort_values("tls.handshake.ja3")
ja3 = ja3.drop_duplicates("flow_id", keep="first")
ja3.to_csv("dataset/ja3_prepared.csv", index=False)