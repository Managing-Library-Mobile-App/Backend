from datetime import datetime
from typing import Any

books: list[dict[str, Any]] = [
    {
        "id": "A",
        "language": "pol",
        "isbn": "0101010101",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Jans House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure", "Fantasy, Science fiction"],
        "picture": "https://picsum.photos/id/1/4579/3271",
        "premiere_date": datetime.strptime("20-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "B",
        "language": "pol",
        "isbn": "0101010546557",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/2/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "C",
        "language": "pol",
        "isbn": "0101010103",
        "title": "The Great Britain",
        "authors": ["BERET", "AMI"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/77/5000/3333",
        "premiere_date": datetime.strptime("21-05-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "V",
        "language": "pol",
        "isbn": "0101010104",
        "title": "The Great Britain",
        "authors": ["AMA", "AMI", "DZJ", "BA", "DZ"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/65/5000/3333",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "X",
        "language": "pol",
        "isbn": "0101010105",
        "title": "The Great Britain",
        "authors": ["ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/5/1920/1280",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 333,
    },
    {
        "id": "Z",
        "language": "pol",
        "isbn": "010101015602",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/94/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 222,
    },
    {
        "id": "D",
        "language": "pol",
        "isbn": "01010101345602",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/95/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "E",
        "language": "pol",
        "isbn": "01010105789102",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/96/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 111,
    },
    {
        "id": "F",
        "language": "pol",
        "isbn": "010101978670102",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/151/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "G",
        "language": "pol",
        "isbn": "010101019802",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/98/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "H",
        "language": "pol",
        "isbn": "0101010189002",
        "title": "The Great Britain",
        "authors": ["BERET", "ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Action & Adventure"],
        "picture": "https://picsum.photos/id/99/200/300",
        "premiere_date": datetime.strptime("21-02-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "I",
        "language": "eng",
        "isbn": "0101010106",
        "title": "The Great Britain",
        "authors": ["ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/6/200/300",
        "premiere_date": datetime.strptime("21-04-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "J",
        "language": "pol",
        "isbn": "0101010107",
        "title": "The Great Britain",
        "authors": ["ANA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/7/1920/1280",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 32,
    },
    {
        "id": "K",
        "language": "eng",
        "isbn": "0101010108",
        "title": "The Great Britain",
        "authors": ["ANA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/8/200/300",
        "premiere_date": datetime.strptime("21-07-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "L",
        "language": "deu",
        "isbn": "0101010109",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/9/1920/1280",
        "premiere_date": datetime.strptime("21-10-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "M",
        "language": "chi",
        "isbn": "t678987654",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/10/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 232,
    },
    {
        "id": "N",
        "language": "chi",
        "isbn": "7890-0987654",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/10/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 133,
    },
    {
        "id": "1",
        "language": "chi",
        "isbn": "657890-987654",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/83/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 122,
    },
    {
        "id": "2",
        "language": "chi",
        "isbn": "4567898765",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/82/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 1231,
    },
    {
        "id": "3",
        "language": "chi",
        "isbn": "5678908765",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/81/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "4",
        "language": "chi",
        "isbn": "86749086",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/111/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 13,
    },
    {
        "id": "5",
        "language": "chi",
        "isbn": "67879654",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Romance"],
        "picture": "https://picsum.photos/id/85/200/300",
        "premiere_date": datetime.strptime("21-11-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "6",
        "language": "pol",
        "isbn": "0101010121",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Drama"],
        "picture": "https://picsum.photos/id/11/200/300",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 123,
    },
    {
        "id": "7",
        "language": "pol",
        "isbn": "0101010131",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Thriller, Horror, Mystery and detective stories"],
        "picture": "https://picsum.photos/id/12/1280/774",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 12,
    },
    {
        "id": "8",
        "language": "pol",
        "isbn": "0101010141",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Politics"],
        "picture": "https://picsum.photos/id/13/5000/2813",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 3,
    },
    {
        "id": "9",
        "language": "pol",
        "isbn": "0101010151",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Law"],
        "picture": "https://picsum.photos/id/14/4106/2806",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 13,
    },
    {
        "id": "10",
        "language": "pol",
        "isbn": "0101010161",
        "title": "The Great Britain",
        "authors": ["AMA"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Comedy"],
        "picture": "https://picsum.photos/id/15/4855/1803",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 23,
    },
    {
        "id": "11",
        "language": "pol",
        "isbn": "0101010171",
        "title": "The Great Britain",
        "authors": ["ANG"],
        "publishing_house": "Adams House",
        "description": "The Great Britain is a great britain book which...",
        "genres": ["Botany"],
        "picture": "https://picsum.photos/id/16/4579/3271",
        "premiere_date": datetime.strptime("21-01-2022", "%d-%m-%Y"),
        "number_of_pages": 12,
    },
]
