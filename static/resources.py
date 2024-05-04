from api.account.change_theme import ChangeTheme
from api.account.change_password import ChangePassword
from api.account.change_profile_picture import ChangeProfilePicture
from api.account.check_if_logged_in import CheckIfLoggedIn
from api.account.delete_account import DeleteAccount
from api.account.logged_in_users import LoggedInUsers
from api.account.login import Login
from api.account.logout import Logout
from api.account.register import Register
from api.data.authors.author import Author
from api.data.books.book import Book
from api.data.bought_books.bought_book import BoughtBook
from api.data.fans.fans import Fan
from api.data.favourite_books.favourite_book import FavouriteBook
from api.data.genres.genres import Genres
from api.data.libraries.library import Library
from api.data.new_books.new_book import NewBook
from api.data.opinions.opinion import Opinion
from api.data.read_books.read_book import ReadBook
from api.data.similar_books.similar_books import SimilarBooks
from api.data.user.user import User
from api.favicon import Favicon
from static.urls import *

RESOURCES = {
    AUTHOR_URL: Author,
    BOOK_URL: Book,
    BOUGHT_BOOK_URL: BoughtBook,
    CHANGE_THEME_URL: ChangeTheme,
    CHANGE_PASSWORD_URL: ChangePassword,
    CHANGE_PROFILE_PICTURE_URL: ChangeProfilePicture,
    CHECK_IF_LOGGED_IN_URL: CheckIfLoggedIn,
    DELETE_ACCOUNT_URL: DeleteAccount,
    FANS_URL: Fan,
    FAVICON_URL: Favicon,
    FAVOURITE_BOOK_URL: FavouriteBook,
    GENRES_URL: Genres,
    LIBRARY_URL: Library,
    LOGIN_URL: Login,
    LOGGED_IN_USERS_URL: LoggedInUsers,
    LOGOUT_URL: Logout,
    NEW_BOOK_URL: NewBook,
    OPINION_URL: Opinion,
    READ_BOOK_URL: ReadBook,
    REGISTER_URL: Register,
    USER_URL: User,
    SIMILAR_BOOKS_URL: SimilarBooks,
}
