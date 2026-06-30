import pandas as pd

df = pd.read_csv("dataset/final_ml_dataset.csv", low_memory=False)

print("\nTamaño:", df.shape)
print("\nNo hay JA3:")
print(df["tls.handshake.ja3"].isna().mean())
print("\nLabels:")
print(df["Label"].value_counts().head(15))
print("\nJA3 por clase:")
print(df.groupby("Label")["tls.handshake.ja3"].apply(lambda x: x.notna().mean()))