import json
import os

import requests


def get_recent_changes(YYYY: str, MM: str = None, DD: str = None):
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

    # Mamy możliwość zupdatować istniejące książki, dodać nowe książki, dodać nowe covery do książek, ale musimy
    # za każdym razem robić jeszcze requesta do openlibrary i pobierać zmiany

    if not DD:
        if not MM:
            LINK_RECENT_CHANGES_ADD_BOOK = (
                f"http://openlibrary.org/recentchanges/{YYYY}/add-book.json"
            )
        else:
            LINK_RECENT_CHANGES_ADD_BOOK = (
                f"http://openlibrary.org/recentchanges/{YYYY}/{MM}/add-book.json"
            )
    else:
        LINK_RECENT_CHANGES_ADD_BOOK = (
            f"http://openlibrary.org/recentchanges/{YYYY}/{MM}/{DD}/add-book.json"
        )

    file_path = os.path.join("received_recent_changes", "recent_changes.json")

    request = requests.get(
        LINK_RECENT_CHANGES_ADD_BOOK.format(YYYY, MM, DD),
        verify=False,
    )
    if request.status_code == 200:
        data = request.json()
        books_with_authors = []
        for change in data:
            if change["kind"] == "add-book":
                book = None
                authors = []
                for changed_object in change["changes"]:
                    if changed_object["key"].startswith("/books/"):
                        book = changed_object["key"]
                    elif changed_object["key"].startswith("/authors/"):
                        authors.append(changed_object["key"])
                books_with_authors.append({book: authors})
        with open(file_path, "w") as f:
            json.dump(books_with_authors, f, indent=4)

    else:
        raise Exception(
            f"Could not log in to the API. Status code: {request.status_code}"
        )


if __name__ == "__main__":
    get_recent_changes("2024", "05", "01")
