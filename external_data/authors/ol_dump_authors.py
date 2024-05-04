import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_authors_2024-03-31.txt")
write_file_path = os.path.join("processed_data_authors", "ol_dump_authors.csv")

if os.path.exists(write_file_path):
    os.remove(write_file_path)

with open(read_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

n = 0
for df in pd.read_csv(
    read_file_path,
    chunksize=100000,
    sep="\t",
    names=["type", "id", "something", "date", "json_data"],
):
    n += 1
    print(f"Batch {n}")
    df.reset_index(drop=True, inplace=True)

    df["json_data"] = df["json_data"].apply(json.loads)
    df_normalized = pd.json_normalize(df["json_data"])
    df_normalized.reset_index(drop=True, inplace=True)
    df = pd.concat([df.drop(columns=["json_data"]), df_normalized], axis="columns")

    df = df[df["id"].notna()]
    df = df[["id", "name", "photos", "bio.value"]]
    df = df[df["name"].notna()]

    df = df.rename(columns={"photos": "picture", "bio.value": "biography"})
    if not os.path.exists(write_file_path):
        df.to_csv(write_file_path, index=False, mode="w")
    else:
        df.to_csv(write_file_path, header=False, index=False, mode="a")

with open(write_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

# id - authors dump 'key' - musi być
# name - authors dump 'name' - musi być
# genres - wypełniam samodzielnie na podstawie books (setem)
# biography - authors dump 'bio' - nie musi być
# picture - authors dump 'photos' - nie musi być
# released_books - edition dump - brane z książek
