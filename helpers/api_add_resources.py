import flask_restful

from api.account.already_logged_in import CheckIfLoggedIn
from api.account.logged_in_users import LoggedInUsers
from api.data.authors.author import Author
from api.data.books.book import Book
from api.data.book_announcements.book_announcement import BookAnnouncement
from api.data.libraries.library import Library
from api.data.opinions.opinion import Opinion
from api.favicon import Favicon
from api.account.change_password import ChangePassword
from api.account.delete_account import DeleteAccount
from api.account.login import Login
from api.account.logout import Logout
from api.account.register import Register


def api_add_resources_v1(api: flask_restful.Api) -> None:
    api_without_version = "/api/"
    account = "account/"
    data = "data/"

    # additional
    api.add_resource(
        Favicon,
        "/favicon.ico",
        endpoint="favicon",
    )

    # account
    api.add_resource(
        Login,
        f"{api_without_version}{account}login",
        endpoint="login",
    )
    api.add_resource(
        Register,
        f"{api_without_version}{account}register",
        endpoint="register",
    )

    api.add_resource(
        ChangePassword,
        f"{api_without_version}{account}change_password",
        endpoint="change_password",
    )
    api.add_resource(
        DeleteAccount,
        f"{api_without_version}{account}delete_account",
        endpoint="delete_account",
    )
    api.add_resource(
        Logout,
        f"{api_without_version}{account}logout",
        endpoint="logout",
    )

    api.add_resource(
        LoggedInUsers,
        f"{api_without_version}{account}logged_in_users",
        endpoint="logged_in_users",
    )

    api.add_resource(
        CheckIfLoggedIn,
        f"{api_without_version}{account}check_if_logged_in",
        endpoint="check_if_logged_in",
    )

    # author
    api.add_resource(
        Author,
        f"{api_without_version}{data}author",
        endpoint="author",
    )

    # book
    api.add_resource(
        Book,
        f"{api_without_version}{data}book",
        endpoint="book",
    )

    # book announcement
    api.add_resource(
        BookAnnouncement,
        f"{api_without_version}{data}book_announcement",
        endpoint="book_announcement",
    )

    # library
    api.add_resource(
        Library,
        f"{api_without_version}{data}library",
        endpoint="library",
    )

    # opinion
    api.add_resource(
        Opinion,
        f"{api_without_version}{data}opinion",
        endpoint="opinion",
    )
