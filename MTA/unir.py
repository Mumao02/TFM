import os
import pandas as pd

BASE_DIR = "/mnt/c/Users/marco/Desktop/uni/MTA"
OUTPUT_FILE = "dataset_ml.csv"

all_data = []

def read_zeek_log(path):

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        lines = f.readlines()

    fields = None
    data = []

    for line in lines:
        line = line.strip()

        if line.startswith("#fields"):
            fields = line.split("\t")[1:]

        elif line.startswith("#"):
            continue

        else:
            parts = line.split("\t")
            if fields and len(parts) == len(fields):
                data.append(parts)

    if fields is None or len(data) == 0:
        return None

    return pd.DataFrame(data, columns=fields)


def load_logs(zeek_dir, label):

    conn_path = os.path.join(zeek_dir, "conn.log")
    ssl_path  = os.path.join(zeek_dir, "ssl.log")

    conn = read_zeek_log(conn_path)

    if conn is None or "uid" not in conn.columns:
        print(f"conn.log inválido en {zeek_dir}")
        return None

    df = conn

    ssl = read_zeek_log(ssl_path)

    if ssl is not None and "uid" in ssl.columns:
        df = df.merge(ssl, on="uid", how="left")

    df["label"] = label
    return df



for dataset in os.listdir(BASE_DIR):

    dataset_path = os.path.join(BASE_DIR, dataset)

    if not os.path.isdir(dataset_path):
        continue

    zeek_root = os.path.join(dataset_path, "zeek")

    if not os.path.isdir(zeek_root):
        continue


    for sample in os.listdir(zeek_root):

        sample_dir = os.path.join(zeek_root, sample)

        if not os.path.isdir(sample_dir):
            continue

        df = load_logs(sample_dir, dataset.upper())

        if df is not None:

            all_data.append(df)

            print(
                f" {sample} -> {len(df)} filas"
            )

        else:

            print(
                f" {sample} -> vacío"
            )


if len(all_data) == 0:
    print("No dataset generado")
    exit(1)

final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df.dropna(axis=1, how="all")
final_df.to_csv(OUTPUT_FILE, index=False)

