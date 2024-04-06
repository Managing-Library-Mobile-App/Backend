from api.data.user.user import User
from static.urls import *
from api.account.change_password import ChangePassword
from api.account.check_if_logged_in import CheckIfLoggedIn
from api.account.delete_account import DeleteAccount
from api.account.logged_in_users import LoggedInUsers
from api.account.login import Login
from api.account.logout import Logout
from api.account.register import Register
from api.data.authors.author import Author
from api.data.book_announcements.book_announcement import BookAnnouncement
from api.data.books.book import Book
from api.data.libraries.library import Library
from api.data.opinions.opinion import Opinion
from api.favicon import Favicon

RESOURCES = {
    FAVICON_URL:  Favicon,
    OPINION_URL:  Opinion,
    LIBRARY_URL:  Library,
    BOOK_ANNOUNCEMENT_URL:  BookAnnouncement,
    BOOK_URL:  Book,
    AUTHOR_URL:  Author,
    USER_URL:  User,
    CHECK_IF_LOGGED_IN_URL:  CheckIfLoggedIn,
    LOGGED_IN_USERS_URL:  LoggedInUsers,
    LOGOUT_URL:  Logout,
    DELETE_ACCOUNT_URL:  DeleteAccount,
    CHANGE_PASSWORD_URL:  ChangePassword,
    REGISTER_URL:  Register,
    LOGIN_URL:  Login
}
