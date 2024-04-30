from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

import requests

from static.urls import *
from test_data.users import admins


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
) -> Generator[None, None, None]:
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
    print(new_author_json)
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
    yield new_book.json()
    # After all
    deleted_book = api_admin_request_context.delete(f"")
    assert deleted_book.ok


def test_add_opinion_to_book(
    api_admin_request_context: APIRequestContext, test_book
) -> None:
    data = {
        "book_id": test_book,
        "stars_count": 4,
        "comment": "good book, Dziuniek approved.",
    }
    print(data)
    new_opinion_request = api_admin_request_context.post(f"", data=data)
    assert new_opinion_request.ok

    opinion_request = api_admin_request_context.get(f"")
    assert opinion_request.ok
    issues_response = opinion_request.json()


def test_should_create_feature_request(
    api_admin_request_context: APIRequestContext,
) -> None:
    data = {
        "title": "[Feature] request 1",
        "body": "Feature description",
    }
    new_issue = api_admin_request_context.post(f"", data=data)
    assert new_issue.ok

    issues = api_admin_request_context.get(f"")
    assert issues.ok
    issues_response = issues.json()


def test_should_create_bug_report(api_admin_request_context: APIRequestContext) -> None:
    books = api_admin_request_context.get(f"{BASE_URL}{BOOK_URL}")
    assert books.ok
    books_json = books.json()
    print(books_json)
    assert books_json
