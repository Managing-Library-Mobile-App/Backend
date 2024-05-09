import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_works_2024-03-31.txt")
write_file_path = os.path.join("processed_data_works", "ol_dump_works.csv")

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

    df = df[
        [
            "id",
            "title",
            "authors",
            "subjects",
            "description.value",
            "first_publish_date",
            "cover_edition.key",
        ]
    ]

    df = df.rename(
        columns={
            "subjects": "genres",
            "description.value": "biography",
            "first_publish_date": "premiere_date",
        }
    )
    if not os.path.exists(write_file_path):
        df.to_csv(write_file_path, index=False, mode="w")
    else:
        df.to_csv(write_file_path, header=False, index=False, mode="a")

with open(write_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))
