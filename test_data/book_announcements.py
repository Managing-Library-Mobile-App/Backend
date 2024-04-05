from datetime import datetime
from typing import Any

book_announcements: list[dict[str, Any]] = [
    {
        "title": "The Great Britain",
        "author": 1,
        "publishing_house": "Adams House",
        "description": "The great britain is an amazing great britain that was a great britain...",
        "genres": ["Action", "Thriller"],
        "picture": "https://picsum.photos/id/24/4855/1803",
        "premiere_date": datetime.strptime("2024-01-21", "%Y-%m-%d"),
    },
    {
        "title": "Potop",
        "author": 1,
        "publishing_house": "Jans House",
        "description": "The great britain is an amazing great britain that was a great britain...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2024-10-21", "%Y-%m-%d"),
    },
    {
        "title": "The Great America",
        "author": 1,
        "publishing_house": "Adams House",
        "description": "The great britain is an amazing great britain that was a great britain...",
        "genres": ["Thriller"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2025-01-21", "%Y-%m-%d"),
    },
    {
        "title": "The Great Poland",
        "author": 2,
        "publishing_house": "Jans House",
        "description": "The great britain is an amazing great britain that was a great britain...",
        "genres": ["Thriller"],
        "picture": "https://picsum.photos/id/40/4106/2806",
        "premiere_date": datetime.strptime("2026-01-21", "%Y-%m-%d"),
    },
    {
        "title": "The Great Great Far",
        "author": 3,
        "publishing_house": "Gothams House",
        "description": "The great britain is an amazing great britain that was a great britain...",
        "genres": ["Fantasy"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2024-10-25", "%Y-%m-%d"),
    },
]
