import json
import os

import pandas as pd

read_file_path = os.path.join("../raw_data", "ol_dump_editions_2024-03-31.txt")
write_file_path = os.path.join("processed_data_editions", "ol_dump_editions_dev.json")

if os.path.exists(write_file_path):
    os.remove(write_file_path)

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
        # "isbn_13",
        "title",
        "authors",
        "publishers",
        "subjects",
        "publish_date",
        # "works",
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
        # "isbn_13",
        "title",
        "authors",
        "publishers",
        "subjects",
        "publish_date",
        # "works",
        "description.value",
        "languages",
        "number_of_pages",
    ]
    for filter_field in filtered_fields:
        if filter_field in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[filter_field].notna()]

    for index in filtered_df.index:
        if (
            len(filtered_df["isbn_10"][index]) == 0
            or len(filtered_df["languages"][index]) == 0
            or len(filtered_df["publishers"][index]) == 0
        ):
            filtered_df.drop(index=[index], inplace=True)
            break
        filtered_languages = []
        for languages in filtered_df["languages"]:
            for language in languages:
                if language["key"] in ["/languages/pol", "/languages/eng"]:
                    filtered_languages.append(language["key"])
        if len(filtered_languages) == 0:
            filtered_df.drop(index=[index], inplace=True)

    for index in filtered_df.index:
        isbn = filtered_df["isbn_10"][index]
        authors = filtered_df["authors"][index]
        publishers = filtered_df["publishers"][index]
        languages = filtered_df["languages"][index]

        authors_list = []
        for author in authors:
            authors_list.append(author["key"])
        filtered_df.at[index, "authors"] = authors_list
        filtered_df.loc[index, "isbn_10"] = isbn[0]
        filtered_df.loc[index, "publishers"] = publishers[0]
        filtered_df.loc[index, "languages"] = languages[0]["key"]

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
    if not os.path.exists(write_file_path):
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="w")
    else:
        filtered_df.to_json(write_file_path, lines=True, orient="records", mode="a")
    print(f"Batch {n} after processing. Size: {filtered_df.shape}")
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
