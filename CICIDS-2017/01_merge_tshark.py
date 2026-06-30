import pandas as pd
import glob

dfs = []

for f in glob.glob("tshark_out2/*.csv"):

    df = pd.read_csv(f, low_memory=False)
    df.columns = [c.strip() for c in df.columns]

    df["pcap_source"] = f
    dfs.append(df)

ja3 = pd.concat(dfs, ignore_index=True)
ja3 = ja3.dropna(subset=[
    "ip.src", "tcp.srcport",
    "ip.dst", "tcp.dstport",
    "tls.handshake.ja3"
])

ja3.to_csv("dataset/ja3_all.csv", index=False)
