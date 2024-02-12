import pandas as pd

file_path = "ol_dump_authors_2023-11-30.txt"


df = pd.read_csv(file_path, sep="\t", nrows=100)

df.to_excel(file_path + "test.xlsx")

print(df)

# Execution time


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
