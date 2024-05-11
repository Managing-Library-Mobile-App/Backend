import json
import os

import requests

_POSSIBLE_KINDS = [
    "add-cover",
    "add-book",
    "edit-book",
    "merge-authors",
    "update",
    "revert",
    "new-account",
    "register",
    "lists",
]
_USEFUL_KINDS = [
    "add-cover",
    "add-book",
    "edit-book",
    "merge-authors",
]
_USED_KINDS = ["add-book"]
_LINK = "http://openlibrary.org/recentchanges/{}/{}/{}.json"


def get_recent_changes(YYYY: str, MM: str = None, DD: str = None):
    if not DD:
        if not MM:
            link_recent_changes_add_book = (
                f"http://openlibrary.org/recentchanges/{YYYY}/add-book.json"
            )
        else:
            link_recent_changes_add_book = (
                f"http://openlibrary.org/recentchanges/{YYYY}/{MM}/add-book.json"
            )
    else:
        link_recent_changes_add_book = (
            f"http://openlibrary.org/recentchanges/{YYYY}/{MM}/{DD}/add-book.json"
        )

    request_recent_changes = requests.get(
        link_recent_changes_add_book.format(YYYY, MM, DD)
    )
    if request_recent_changes.status_code == 200:
        changes = request_recent_changes.json()
        books_with_authors = []
        for change in changes:
            if change["kind"] == "add-book":
                book = None
                authors = []
                for changed_object in change["changes"]:
                    if changed_object["key"].startswith("/books/"):
                        book = changed_object["key"]
                    elif changed_object["key"].startswith("/authors/"):
                        authors.append(changed_object["key"])
                books_with_authors.append({book: authors})
        with open(
            os.path.join("received_recent_changes", "recent_changes.json"), "w"
        ) as f:
            json.dump(books_with_authors, f, indent=4)

        new_books = []
        new_authors = []
        for book_with_authors in books_with_authors:
            for book, authors in book_with_authors.items():
                request_book = requests.get(f"https://openlibrary.org{book}.json")
                if request_book.status_code == 200:
                    book_data = request_book.json()
                    new_books.append(book_data)
                else:
                    print(
                        f"Could not get an author. Status code: {request_book.status_code}"
                    )
                for author in authors:
                    request_author = requests.get(
                        f"https://openlibrary.org{author}.json"
                    )
                    if request_author.status_code == 200:
                        author_data = request_author.json()
                        new_authors.append(author_data)
                    else:
                        print(
                            f"Could not get an author. Status code: {request_author.status_code}"
                        )

        with open(os.path.join("received_recent_changes", "new_books.json"), "w") as f:
            json.dump(new_books, f, indent=4)
        with open(
            os.path.join("received_recent_changes", "new_authors.json"), "w"
        ) as f:
            json.dump(new_authors, f, indent=4)

        filtered_fields_authors = [
            "key",
            "name",
            "photos",
            "bio",
            "birth_date",
        ]
        filtered_authors = []
        for author in new_authors:
            all_fields_present = False
            for key, value in author.items():
                print(key)
                all_fields_present = True
                if key not in filtered_fields_authors:
                    all_fields_present = False
                    break
            if all_fields_present:
                filtered_authors.append(author)

        filtered_fields_books = [
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
        filtered_books = []
        for book in new_books:
            all_fields_present = False
            for key, value in book.items():
                print(key)
                all_fields_present = True
                if key not in filtered_fields_books:
                    all_fields_present = False
                    break
            if all_fields_present:
                filtered_books.append(book)

        with open(
            os.path.join("received_recent_changes", "filtered_books.json"), "w"
        ) as f:
            json.dump(filtered_books, f, indent=4)
        with open(
            os.path.join("received_recent_changes", "filtered_authors.json"), "w"
        ) as f:
            json.dump(filtered_authors, f, indent=4)
    else:
        raise Exception(
            f"Could not log in to the API. Status code: {request_recent_changes.status_code}"
        )


if __name__ == "__main__":
    get_recent_changes("2024", "05", "01")
