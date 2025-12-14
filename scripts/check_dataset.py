import pandas as pd

csv_path = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\resume_images_labels.csv"
df = pd.read_csv(csv_path)

print("\nTotal images:", len(df))
print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nSample rows:")
print(df.head())
