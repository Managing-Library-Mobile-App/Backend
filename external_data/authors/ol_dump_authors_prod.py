import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_authors_2024-03-31.txt")
write_file_path = os.path.join("processed_data_authors", "ol_dump_authors_prod.json")

if os.path.exists(write_file_path):
    raise Exception("DO NOT OVERWRITE DATA! REMOVE THE FILE IF YOU WANT THAT")

# 13 million authors

n = 0
for df in pd.read_csv(
    read_file_path,
    chunksize=100000,
    sep="\t",
    names=["type", "id", "something", "date", "json_data"],
):
    n += 1
    print(f"Batch {n}. Size: {df.shape}")
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
        else:
            filtered_df[column] = pd.Series()

    filtered_fields = [
        "id",
        "name",
    ]
    for filter_field in filtered_fields:
        if filter_field in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_field].notna()]

    for index in filtered_df.index:
        photos = filtered_df["photos"][index]
        if isinstance(photos, list):
            if photos[0] == -1:
                photos = None
            else:
                photos = photos[0]
            filtered_df.loc[index, "photos"] = photos

    columns_to_rename = {"photos": "picture", "bio.value": "biography"}
    for key in columns_to_rename.keys():
        if key in filtered_df.columns:
            filtered_df = filtered_df.rename(columns={key: columns_to_rename[key]})

    for index in filtered_df.index:
        if filtered_df["picture"][index]:
            filtered_df.loc[
                index, "picture"
            ] = f" https://covers.openlibrary.org/a/id/{filtered_df['picture'][index]}-M.jpg"

    if not os.path.exists(write_file_path):
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="w")
    else:
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="a")
    print(f"Batch {n} after processing. Size: {filtered_df.shape}")

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
