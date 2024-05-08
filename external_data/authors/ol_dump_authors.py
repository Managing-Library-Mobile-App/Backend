import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_authors_2024-03-31.txt")
write_file_path = os.path.join("processed_data_authors", "ol_dump_authors.json")

if os.path.exists(write_file_path):
    os.remove(write_file_path)

# 13 million authors

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
        "name",
        "photos",
        "bio.value",
        "death_date",
        "birth_date",
        "location",
        "website",
    ]
    for column in columns:
        if column in df.columns:
            filtered_df = pd.concat([filtered_df, df[column]], axis="columns")

    filtered_fields = [
        "id",
        "name",
    ]
    for filter_field in filtered_fields:
        if filter_field in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_field].notna()]

    filtered_df = filtered_df.rename(
        columns={"photos": "picture", "bio.value": "biography"}
    )
    if not os.path.exists(write_file_path):
        filtered_df.to_json(
            write_file_path, lines=True, orient="records", index=False, mode="w"
        )
    else:
        filtered_df.to_json(
            write_file_path, lines=True, orient="records", index=False, mode="a"
        )

with open(write_file_path, encoding="utf8") as f:
    print(sum(1 for line in f))

# id - authors dump 'key' - musi być
# name - authors dump 'name' - musi być
# genres - wypełniam samodzielnie na podstawie books (setem)
# biography - authors dump 'bio' - nie musi być
# picture - authors dump 'photos' - nie musi być
# released_books - edition dump - brane z książek
# death_date - authors dump 'death_date' - nie musi być
# birth_date - authors dump 'birth_date' - nie musi być
# location - authors dump 'location' - nie musi być
# website - authors dump 'website' - nie musi być
