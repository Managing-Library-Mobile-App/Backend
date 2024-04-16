from api.account.change_password import ChangePassword
from api.account.check_if_logged_in import CheckIfLoggedIn
from api.account.delete_account import DeleteAccount
from api.account.logged_in_users import LoggedInUsers
from api.account.login import Login
from api.account.logout import Logout
from api.account.register import Register
from api.data.authors.author import Author
from api.data.books.book import Book
from api.data.books.genres import Genres
from api.data.books.new_book import NewBook
from api.data.libraries.library import Library
from api.data.opinions.opinion import Opinion
from api.data.user.user import User
from api.favicon import Favicon
from static.urls import *

RESOURCES = {
    AUTHOR_URL: Author,
    BOOK_URL: Book,
    DELETE_ACCOUNT_URL: DeleteAccount,
    FAVICON_URL: Favicon,
    OPINION_URL: Opinion,
    LIBRARY_URL: Library,
    USER_URL: User,
    CHECK_IF_LOGGED_IN_URL: CheckIfLoggedIn,
    LOGGED_IN_USERS_URL: LoggedInUsers,
    LOGOUT_URL: Logout,
    CHANGE_PASSWORD_URL: ChangePassword,
    REGISTER_URL: Register,
    LOGIN_URL: Login,
    GENRES_URL: Genres,
    NEW_BOOK_URL: NewBook,
}
