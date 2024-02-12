import pandas as pd

file_path = "ol_dump_editions_2023-11-30.txt"

df = pd.read_csv(file_path, sep="\t", nrows=100)

df.to_excel(file_path + "test.xlsx")

print(df)

# TODO przetworzyć dane do innego pliku z tylko potrzebnymi danymi (kolumnami)


# type - type of record (/type/edition, /type/work etc.) NOT NEEDED
# key - unique key of the record. (/books/OL1M etc.)
# revision - revision number of the record NOT NEEDED
# last_modified - last modified timestamp NOT NEEDED
# JSON - the complete record in JSON format:::::::::::::::::::
# title of type /type/string
# title_prefix of type /type/string NOT NEEDED
# subtitle of type /type/string NOT NEEDED
# other_titles[] of type /type/string NOT NEEDED
# authors[] of type /type/author
# by_statement of type /type/string NOT NEEDED
# publish_date of type /type/string
# copyright_date of type /type/string NOT NEEDED
# edition_name of type /type/string NOT NEEDED
# languages[] of type /type/language NOT NEEDED
# description of type /type/text
# notes of type /type/text NOT NEEDED
# genres[] of type /type/string
# table_of_contents[] of type /type/toc_item NOT NEEDED
# work_titles[] of type /type/string NOT NEEDED
# series[] of type /type/string NOT NEEDED
# physical_dimensions of type /type/string NOT NEEDED
# physical_format of type /type/string NOT NEEDED
# number_of_pages of type /type/int NOT NEEDED
# subjects[] of type /type/string
# pagination of type /type/string NOT NEEDED
# lccn[] of type /type/string NOT NEEDED
# ocaid of type /type/string NOT NEEDED
# oclc_numbers[] of type /type/string NOT NEEDED
# isbn_10[] of type /type/string
# isbn_13[] of type /type/string
# dewey_decimal_class[] of type /type/string NOT NEEDED
# lc_classifications[] of type /type/string NOT NEEDED
# contributions[] of type /type/string
# publish_places[] of type /type/string NOT NEEDED
# publish_country of type /type/string NOT NEEDED
# publishers[] of type /type/string
# distributors[] of type /type/string NOT NEEDED
# first_sentence of type /type/text
# weight of type /type/string
# location[] of type /type/string NOT NEEDED
# scan_on_demand of type /type/boolean NOT NEEDED
# collections[] of type /type/collection NOT NEEDED
# uris[] of type /type/string NOT NEEDED
# uri_descriptions[] of type /type/string NOT NEEDED
# translation_of of type /type/string NOT NEEDED
# works[] of type /type/work NOT NEEDED
# source_records[] of type /type/string NOT NEEDED
# translated_from[] of type /type/language NOT NEEDED
# scan_records[] of type /type/scan_record NOT NEEDED
# volumes[] of type /type/volume NOT NEEDED
# accompanying_material of type /type/string NOT NEEDED
