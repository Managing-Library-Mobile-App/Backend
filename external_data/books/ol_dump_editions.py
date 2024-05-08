import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_editions_2024-03-31.txt")
write_file_path = os.path.join("processed_data_editions", "ol_dump_editions.json")

if os.path.exists(write_file_path):
    os.remove(write_file_path)

# 45 million editions

n = 0
for df in pd.read_csv(
    read_file_path,
    chunksize=1000000,
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

    filtered_df = pd.DataFrame()
    columns = [
        "id",
        "isbn_10",
        "isbn_13",
        "title",
        "authors",
        "publishers",
        "subjects",
        "publish_date",
        "works",
        "description.value",
        "languages",
        "number_of_pages",
    ]
    for column in columns:
        if column in df.columns:
            filtered_df = pd.concat([filtered_df, df[column]], axis="columns")

    filtered_fields = [
        "id",
        "isbn_10",
        "title",
        "authors",
        "publishers",
        "description.value",
        "subjects",
        "publish_date",
        "languages",
        "number_of_pages",
    ]
    for filter_field in filtered_fields:
        if filter_field in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_field].notna()]
    filtered_df = filtered_df[filtered_df["id"].notna()]
    filtered_df.drop(columns=["isbn_10"])

    filtered_df = filtered_df.rename(
        columns={
            "publish_date": "premiere_date",
            "description.value": "description",
            "languages": "language",
            "subjects": "genres",
            "publishers": "publishing_house",
            "isbn_10": "isbn",
        }
    )
    if not os.path.exists(write_file_path):
        filtered_df.to_json(
            write_file_path, lines=True, orient="records", index=False, mode="w"
        )
    else:
        filtered_df.to_json(
            write_file_path, lines=True, orient="records", index=False, mode="a"
        )
    # pd.read_json('output.json',orient='records',lines=True)
    # filtered_df = filtered_df[
    #     filtered_df["isbn_10"].notna() | filtered_df["isbn_13"].notna()
    # ]


with open(write_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

# id - edition dump - id - musi być
# isbn - edition dump - isbn_10 lub isbn_13 (musi być conajmniej 1 z tych 2, a w pierwszej kolejności bierzemy isbn_13)
# title - edition dump - musi być
# authors - edition dump - musi być
# publishing_house - edition dump - musi być
# description - edition dump - musi być
# genres - subjects z edition dump - musi być
# premiere_date - edition dump - musi być
# language - edition dump - musi być
# works - musi być
# number of pages - musi być
