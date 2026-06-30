import pandas as pd

cic = pd.read_csv("dataset/trafficlabelling_completo.csv", low_memory=False)
ja3 = pd.read_csv("dataset/ja3_prepared.csv", low_memory=False)

def flow_key(ip1, p1, ip2, p2):
    try:
        p1 = int(float(p1))
        p2 = int(float(p2))
    except:
        return None

    a = f"{ip1}:{p1}-{ip2}:{p2}"
    b = f"{ip2}:{p2}-{ip1}:{p1}"
    return min(a, b)

cic["flow_id"] = cic.apply(
    lambda r: flow_key(
        r["Source IP"], r["Source Port"],
        r["Destination IP"], r["Destination Port"]
    ),
    axis=1
)

ja3 = ja3[["flow_id", "tls.handshake.ja3", "tls.handshake.extensions_server_name"]]

df = cic.merge(ja3, on="flow_id", how="left")
coverage = df["tls.handshake.ja3"].notna().mean()

df.to_csv("dataset/final_ml_dataset.csv", index=False)