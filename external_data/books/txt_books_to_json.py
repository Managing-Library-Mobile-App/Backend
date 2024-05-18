import argparse
import json
import os

import pandas as pd

arg_parser = argparse.ArgumentParser(description="Description of your script")
arg_parser.add_argument(
    "type_of_db",
    type=str,
    help="Type of db. Currently used: 'prod' or 'dev'",
)
args = arg_parser.parse_args()
database: str = args.type_of_db

read_file_path = os.path.join(
    "external_data", "raw_data", "ol_dump_editions_2024-04-30.txt"
)
if database == "prod":
    write_file_path = os.path.join(
        "external_data",
        "books",
        "processed_data_editions",
        "ol_dump_editions_prod.json",
    )
else:
    write_file_path = os.path.join(
        "external_data", "books", "processed_data_editions", "ol_dump_editions_dev.json"
    )

if os.path.exists(write_file_path):
    raise Exception("DO NOT OVERWRITE DATA! REMOVE THE FILE IF YOU WANT THAT")

# 45 million editions

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
        "isbn_10",
        "isbn_13",
        "title",
        "authors",
        "publishers",
        "subjects",
        "publish_date",
        "description.value",
        "languages",
        "number_of_pages",
    ]
    for column in columns:
        if column in df.columns:
            filtered_df = pd.concat([filtered_df, df[column]], axis="columns")

    if database == "prod":
        filtered_fields = [
            "id",
            "title",
            "authors",
            "publishers",
            "subjects",
            "publish_date",
            "languages",
            "number_of_pages",
        ]
    else:
        filtered_fields = [
            "id",
            "title",
            "authors",
            "publishers",
            "subjects",
            "publish_date",
            "description.value",
            "languages",
            "number_of_pages",
        ]
    for filter_field in filtered_fields:
        if filter_field in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_field].notna()]
        else:
            filtered_df[filter_field] = pd.Series()

    filtered_df = filtered_df[
        filtered_df["isbn_10"].notna() | filtered_df["isbn_13"].notna()
    ]

    for index in filtered_df.index:
        row = filtered_df.loc[[index]]
        if len(row["languages"][index]) == 0 or len(row["publishers"][index]) == 0:
            filtered_df.drop(index=[index], inplace=True)
            continue
        if isinstance(row["isbn_10"][index], list):
            if row["isbn_10"][index]:
                filtered_df.loc[index, "isbn_10"] = row["isbn_10"][index][0]
            else:
                filtered_df.drop(index=[index], inplace=True)
                continue
        elif isinstance(row["isbn_13"][index], list):
            if row["isbn_10"][index]:
                filtered_df.loc[index, "isbn_10"] = row["isbn_13"][index][0]
            else:
                filtered_df.drop(index=[index], inplace=True)
                continue
        filtered_language = None
        for languages in row["languages"]:
            for language in languages:
                if language["key"] in ["/languages/pol", "/languages/eng"]:
                    filtered_language = language["key"]
        if not filtered_language:
            filtered_df.drop(index=[index], inplace=True)
            continue
        isbn = row["isbn_10"][index]
        authors = row["authors"][index]
        publishers = row["publishers"][index]
        language = row["languages"][index]

        filtered_df.at[index, "authors"] = [author["key"] for author in authors]
        filtered_df.loc[index, "publishers"] = publishers[0]
        filtered_df.loc[index, "languages"] = filtered_language

    df = df.drop("isbn_13", axis=1)
    columns_to_rename = {
        "publish_date": "premiere_date",
        "description.value": "description",
        "languages": "language",
        "subjects": "genres",
        "publishers": "publishing_house",
        "isbn_10": "isbn",
    }
    for key in columns_to_rename.keys():
        if key in filtered_df.columns:
            filtered_df = filtered_df.rename(columns={key: columns_to_rename[key]})

    filtered_df["picture"] = pd.Series()
    for index in filtered_df.copy().index:
        filtered_df.loc[
            index, "picture"
        ] = f"https://covers.openlibrary.org/b/isbn/{filtered_df['isbn'][index]}-M.jpg"

    if not os.path.exists(write_file_path):
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="w")
    else:
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="a")
    print(f"Batch {n} after processing. Size: {filtered_df.shape}")

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
