from typing import Any

libraries: list[dict[str, Any]] = [
    {
        "read_books": ["A", "B", "C"],
        "favourite_books": ["A", "D"],
        "bought_books": ["E"],
    },
    {"read_books": ["A"], "favourite_books": ["B"], "bought_books": ["C"]},
    {
        "read_books": ["F", "G", "A"],
        "favourite_books": ["B", "C", "A"],
        "bought_books": ["C", "B", "A"],
    },
    {"read_books": ["A"], "favourite_books": [], "bought_books": []},
    {"read_books": [], "favourite_books": [], "bought_books": []},
]
