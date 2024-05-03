import os
import sys

# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

import requests
from test_data.users import admins
from static.urls import *


@pytest.fixture(scope="session")
def api_admin_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request = requests.post(
        f"{BASE_URL}{LOGIN_URL}",
        json={"email": admins[0]["email"], "password": admins[0]["password"]},
        verify=False,
    )
    if request.status_code == 200:
        token = request.json()["token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        request_context = playwright.request.new_context(
            base_url=BASE_URL, extra_http_headers=headers, ignore_https_errors=True
        )
        yield request_context
        request_context.dispose()
    else:
        raise Exception(
            f"Could not log in to the API. Status code: {request.status_code}"
        )


@pytest.fixture(scope="session", autouse=True)
def test_book(
    api_admin_request_context: APIRequestContext,
) -> dict:
    # Before all
    new_author = api_admin_request_context.post(
        f"{BASE_URL}{AUTHOR_URL}",
        data={
            "name": "Maciej z klanu",
            "genres": ["Romance", "Thriller"],
            "biography": "Jestem Maciej dobry ze mnie faciej",
            "picture": "https://picsum.photos/id/1027/2848/4272",
        },
    )
    new_author_json = new_author.json()
    new_book = api_admin_request_context.post(
        f"{BASE_URL}{BOOK_URL}",
        data={
            "book_language": "pol",
            "isbn": "0231010191",
            "title": "The Great Bułekkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
            "authors": [new_author_json["id"]],
            "publishing_house": "Adams House",
            "description": "The Great Bułek is a great Bułek book which...",
            "genres": ["Comedy"],
            "picture": "https://picsum.photos/id/24/4855/1803",
            "premiere_date": "2022-01-21",
        },
    )
    assert new_book.ok
    new_book_json = new_book.json()
    yield new_book_json
    # After all
    deleted_book_response = api_admin_request_context.delete(
        f"{BASE_URL}{BOOK_URL}", data={"id": new_book_json["id"]}
    )
    assert deleted_book_response.ok


@pytest.fixture(scope="session", autouse=True)
def test_author(
    api_admin_request_context: APIRequestContext,
) -> dict:
    # Before all
    new_author = api_admin_request_context.post(
        f"{BASE_URL}{AUTHOR_URL}",
        data={
            "name": "Maciej z klanu",
            "genres": ["Romance", "Thriller"],
            "biography": "Jestem Maciej dobry ze mnie faciej",
            "picture": "https://picsum.photos/id/1027/2848/4272",
        },
    )
    new_author_json = new_author.json()
    yield new_author_json
    deleted_author_response = api_admin_request_context.delete(
        f"{BASE_URL}{AUTHOR_URL}", data={"id": new_author_json["id"]}
    )
    assert deleted_author_response.ok


@pytest.fixture(scope="session", autouse=True)
def test_user(
    api_admin_request_context: APIRequestContext,
    playwright: Playwright,
) -> dict:
    # Before all
    api_admin_request_context.post(
        f"{BASE_URL}{REGISTER_URL}",
        data={
            "username": "Maciej-klanu",
            "password": "Romance-123",
            "email": "maciej@maciej.com",
        },
    )
    logged_in_new_user_request = api_admin_request_context.post(
        f"{BASE_URL}{LOGIN_URL}",
        data={
            "email": "maciej@maciej.com",
            "password": "Romance-123",
        },
    )
    token = logged_in_new_user_request.json()["token"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    user_request_context = playwright.request.new_context(
        base_url=BASE_URL, extra_http_headers=headers, ignore_https_errors=True
    )
    user_data_request = user_request_context.get(
        f"{BASE_URL}{USER_URL}?get_self=true",
    )
    yield user_data_request.json()
    # After all
    deleted_author_response = user_request_context.delete(
        f"{BASE_URL}{DELETE_ACCOUNT_URL}",
        data={"password": "Romance-123"},
    )
    print(deleted_author_response.json())
    user_request_context.dispose()
    assert deleted_author_response.ok


def test_add_opinion_to_book(
    api_admin_request_context: APIRequestContext, test_book, test_author, test_user
) -> None:
    data = {
        "book_id": test_book["id"],
        "stars_count": 4,
        "comment": "good book, Dziuniek approved.",
    }
    new_opinion_request = api_admin_request_context.post(
        f"{BASE_URL}{OPINION_URL}", data=data
    )
    assert new_opinion_request.ok
    opinion_request = api_admin_request_context.get(f"{BASE_URL}{OPINION_URL}")
    assert opinion_request.ok
    opinion_request_json = opinion_request.json()
    assert opinion_request_json["results"][0] == {
        "book_id": data["book_id"],
        "comment": data["comment"],
        "id": opinion_request_json["results"][0]["id"],
        "profile_picture": test_user["results"][0]["profile_picture"],
        "stars_count": data["stars_count"],
        "user_id": 1,
        "username": "AdminAdmin-1234",
    }


def test_should_create_book_request(
    api_admin_request_context: APIRequestContext,
) -> None:
    data = {
        "book_language": "pol",
        "isbn": "0231010191",
        "title": "The Great Bułekkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        "authors": [1],
        "publishing_house": "Adams House",
        "description": "The Great Bułek is a great Bułek book which...",
        "genres": ["Comedy"],
        "picture": "https://picsum.photos/id/24/4855/1803",
        "premiere_date": "2022-01-21",
    }
    new_book = api_admin_request_context.post(f"{BASE_URL}{BOOK_URL}", data=data)
    assert new_book.ok


def test_should_get_all_books(api_admin_request_context: APIRequestContext) -> None:
    books = api_admin_request_context.get(f"{BASE_URL}{BOOK_URL}")
    assert books.ok
    books_json = books.json()
    assert books_json
