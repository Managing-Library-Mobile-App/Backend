import json

import pandas as pd

file_path = "ol_dump_editions_2023-11-30.txt"


df = pd.read_csv(
    file_path,
    sep="\t",
    nrows=100,
    names=["type", "id", "something", "date", "json_data"],
)

print(df)

df["json_data"] = df["json_data"].apply(json.loads)

# Convert dictionaries into DataFrame columns
df_normalized = pd.json_normalize(df["json_data"])

print(df_normalized)

# Concatenate the new DataFrame with the original DataFrame, dropping the JSON column
df = pd.concat([df.drop(columns=["json_data"]), df_normalized], axis=1)

df.drop(
    columns=[
        "type",
        "something",
        "physical_format",
        "number_of_pages",
        "key",
        "latest_revision",
        "oclc_numbers",
        "works",
        "revision",
        "last_modified.type",
        "last_modified.value",
        "created.type",
        "created.value",
        "type.key",
        "source_records",
        "subtitle",
        "series",
        "covers",
        "lc_classifications",
        "ocaid",
        "publish_places",
        "pagination",
        "dewey_decimal_class",
        "languages",
        "lccn",
        "publish_country",
        "by_statement",
        "local_id",
        "notes.type",
        "notes.value",
        "identifiers.goodreads",
        "contributions",
        "other_titles",
        "subject_place",
        "identifiers.librarything",
        "subject_time",
        "uri_descriptions",
        "url",
        "uris",
    ],
    inplace=True,
)

print(df)


# Execution time

df.reset_index(inplace=True, drop=True)
df.to_csv("ol_dump_editions.csv", index=True, index_label="index")
df.to_excel(file_path + "test.xlsx")


# type - type of record (/type/edition, /type/work etc.) NOT NEEDED
# key - unique key of the record. (/books/OL1M etc.)
# revision - revision number of the record NOT NEEDED
# last_modified - last modified timestamp NOT NEEDED
# JSON - the complete record in JSON format:::::::::::::::::::
# name of type /type/string
# eastern_order of type /type/boolean NOT NEEDED
# personal_name of type /type/string
# enumeration of type /type/string NOT NEEDED
# title of type /type/string
# alternate_names[] of type /type/string NOT NEEDED
# uris[] of type /type/string NOT NEEDED
# bio of type /type/text
# location of type /type/string
# birth_date of type /type/string
# death_date of type /type/string
# date of type /type/string NOT NEEDED
# wikipedia of type /type/string NOT NEEDED
# links[] of type /type/link NOT NEEDED
# Backreferences
# books from /type/edition.authors NOT NEEDED?
# works from /type/work.authors NOT NEEDED?
