from typing import Any

libraries: list[dict[str, Any]] = [
    {
        "read_books": ["AMA", "AMI", "DZ"],
        "favourite_books": ["AMA", "AMI"],
        "bought_books": ["DZ"],
    },
    {"read_books": ["AMA"], "favourite_books": ["AMA"], "bought_books": ["AMA"]},
    {
        "read_books": ["AMA", "AMI", "DZ"],
        "favourite_books": ["AMA", "AMI", "DZ"],
        "bought_books": ["AMA", "AMI", "DZ"],
    },
    {"read_books": ["AMA"], "favourite_books": [], "bought_books": []},
    {"read_books": [], "favourite_books": [], "bought_books": []},
]
