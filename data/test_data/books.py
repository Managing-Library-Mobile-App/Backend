from datetime import datetime

books = [
    {
        "isbn": "01010101010101",
        "title": "The Great Britain",
        "author": 1,
        "publishing_house": "Jans House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/1084/4579/3271",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010102",
        "title": "The Great Britain",
        "author": 1,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-02-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010103",
        "title": "The Great Britain",
        "author": 1,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-05-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010104",
        "title": "The Great Britain",
        "author": 2,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/1084/4579/3271",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010105",
        "title": "The Great Britain",
        "author": 2,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action"],
        "picture": "https://picsum.photos/id/200/1920/1280",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010106",
        "title": "The Great Britain",
        "author": 2,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-04-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010107",
        "title": "The Great Britain",
        "author": 3,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/200/1920/1280",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010108",
        "title": "The Great Britain",
        "author": 4,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-07-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010109",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/200/1920/1280",
        "premiere_date": datetime.strptime("2022-10-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010111",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-11-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010121",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Drama"],
        "picture": "https://picsum.photos/id/237/200/300",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010131",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Horror"],
        "picture": "https://picsum.photos/id/85/1280/774",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010141",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Politics"],
        "picture": "https://picsum.photos/id/63/5000/2813",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010151",
        "title": "The Great Britain",
        "author": 5,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Law"],
        "picture": "https://picsum.photos/id/40/4106/2806",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010161",
        "title": "The Great Britain",
        "author": 3,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Comedy"],
        "picture": "https://picsum.photos/id/24/4855/1803",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
    {
        "isbn": "01010101010171",
        "title": "The Great Britain",
        "author": 2,
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Botany"],
        "picture": "https://picsum.photos/id/1084/4579/3271",
        "premiere_date": datetime.strptime("2022-01-21", "%Y-%m-%d"),
    },
]

# TODO NA PODSTAWIE DANYCH WYBRAĆ 24 najpopularniejsze kategorie
#  i zrobić z nich enuma, a resztę dać jako 25 - other