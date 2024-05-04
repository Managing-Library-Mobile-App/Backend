import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_editions_2024-03-31.txt")
write_file_path = os.path.join("processed_data_editions", "ol_dump_editions.csv")

if os.path.exists(write_file_path):
    os.remove(write_file_path)

with open(read_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

n = 0
for df in pd.read_csv(
    read_file_path,
    chunksize=10000,
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
            "isbn_10",
            "isbn_13",
            "title",
            "authors",
            "publishers",
            "subjects",
            "publish_date",
            "works",
        ]
    ]

    df = df[df["id"].notna()]
    df = df[df["title"].notna()]
    # df = df.drop(df["isbn_10"].isna() & df["isbn_13"].isna())
    print(df.shape)
    df_with_isbn_10 = df[df["isbn_10"].notna()]
    print(df_with_isbn_10.shape)
    df_with_isbn_13 = df[df["isbn_13"].notna()]
    print(df_with_isbn_13.shape)
    # df = df[df["isbn_10"].notna() or df["isbn_13"].notna()]
    df = df[df["authors"].notna()]
    df = df[df["description"].notna()]
    df = df[df["publish_date"].notna()]
    df = df[df["language"].notna()]
    df = df[df["works"].notna()]

    # isbn_10 and isbn_13 do jednej kolumny i zmienic nazwę i usunąć pozostałe

    df = df.rename(columns={"publish_date": "premiere_date", "bio.value": "biography"})
    if not os.path.exists(write_file_path):
        df.to_csv(write_file_path, index=False, mode="w")
    else:
        df.to_csv(write_file_path, header=False, index=False, mode="a")

with open(write_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

# id - edition dump - id - musi być
# isbn - edition dump - isbn_10 lub isbn_13 (musi być conajmniej 1 z tych 2, a w pierwszej kolejności bierzemy isbn_13)
# title - edition dump - musi być
# authors - edition dump - musi być
# publishing_house - edition dump - nie musi być
# description - edition dump - musi być
# genres - subjects z edition dump - nie musi być
# premiere_date - edition dump - musi być
# language - edition dump - musi być
# works - musi być
