# Static
PASSWORD_WRONG_FORMAT_RESPONSE = (
    {
        "message": "password_wrong_format",
        "details": """Wrong password format. Password should have from 10 to 50 characters.
                It should contain at least one upper letter, at least 1 lower letter, at least 1 number and
                at least one special character""",
    },
    403,
)
PASSWORD_CHANGED_RESPONSE = {
    "message": "password_changed",
    "details": "Password changed",
}, 200

PASSWORD_NOT_CHANGED_RESPONSE = {
    "message": "wrong_password",
    "details": "Wrong password",
}, 401
TOKEN_INVALID_RESPONSE = {
    "message": "token_invalid",
    "details": "Token invalid",
}, 401
TOKEN_VALID_RESPONSE = {
    "message": "token_valid",
    "details": "Token valid",
}, 200
CANNOT_DELETE_ADMIN_RESPONSE = {
    "message": "cannot_delete_admin",
    "details": "Admin account cannot be deleted",
}, 401

USER_DELETED_RESPONSE = {
    "message": "user_deleted",
    "details": "User deleted successfully",
}, 200
USER_DOES_NOT_EXIST_RESPONSE = {
    "message": "user_does_not_exist",
    "details": "User does not exist",
}, 404
AUTHOR_DOES_NOT_EXIST_RESPONSE = {
    "message": "author_does_not_exist",
    "details": "Author does not exist",
}, 404
FAN_DOES_NOT_EXIST_RESPONSE = {
    "message": "fan_does_not_exist",
    "details": "Fan does not exist",
}, 404
WRONG_SECRET_RESPONSE = {
    "message": "wrong_secret",
    "details": "Wrong secret field value. Cannot view logged in users.",
}, 401
WRONG_LOGIN_PARAMS_COMBINATION = {
    "message": "wrong_login_params_combination",
    "details": "Cannot pass both user_id and get_self",
}, 401
LOGGED_OUT_RESPONSE = {
    "message": "logged_out",
    "details": "Logged out",
}, 200
NOT_LOGGED_OUT_RESPONSE = {
    "message": "not_logged_out",
    "details": "Could not log out. User was not logged in.",
}, 200
USER_NOT_LOGGED_IN_RESPONSE = {
    "message": "authentication_failed",
    "details": "Authentication failed. Wrong email or password",
}, 401
LOCKED_USER_LOGIN_ATTEMPTS_RESPONSE = {
    "message": "locked_user_login_attempts",
    "details": "User locked because of too many unsuccessful attempts",
}, 401
USERNAME_WRONG_FORMAT_RESPONSE = {
    "message": "username_wrong_format",
    "details": "Wrong username format. It should be from 10 to 50 characters "
    "and it can only contain upper letters, lower letters, "
    "numbers and signs: - and _",
}, 401
EMAIL_WRONG_FORMAT_RESPONSE = {
    "message": "email_wrong_format",
    "details": "Wrong email format.",
}, 401
WRONG_DATE_FORMAT_RESPONSE = {
    "message": "date_wrong_format",
    "details": "Wrong date format. Use YYYY-MM-DD HH:MM:SS",
}, 401
USER_NOT_FOUND_RESPONSE = {
    "message": "user_not_found",
    "details": "User logged in with such token not found",
}, 404
BOOK_NOT_FOUND_RESPONSE = {
    "message": "book_not_found",
    "details": "Book not found",
}, 404
BOOK_NOT_IN_READ_BOOKS_RESPONSE = {
    "message": "book_not_in_read_books",
    "details": "Book not in read books",
}, 404
BOOK_NOT_IN_FAVOURITE_BOOKS_RESPONSE = {
    "message": "book_not_in_favourite_books",
    "details": "Book not in favourite books",
}, 404
BOOK_NOT_IN_BOUGHT_BOOKS_RESPONSE = {
    "message": "book_not_in_bought_books",
    "details": "Book not in bought books",
}, 404
BOOK_ALREADY_IN_READ_BOOKS_RESPONSE = {
    "message": "book_already_in_read_books",
    "details": "Book already in read books",
}, 400
BOOK_ALREADY_IN_FAVOURITE_BOOKS_RESPONSE = {
    "message": "book_already_in_favourite_books",
    "details": "Book already in favourite books",
}, 400
BOOK_ALREADY_IN_BOUGHT_BOOKS_RESPONSE = {
    "message": "book_already_in_bought_books",
    "details": "Book already in bought books",
}, 400
USER_ALREADY_IN_FANS_RESPONSE = {
    "message": "user_already_in_fans",
    "details": "User already in fans",
}, 400
AUTHOR_NOT_FOUND_RESPONSE = {
    "message": "author_not_found",
    "details": "Author not found",
}, 404
LIBRARY_NOT_FOUND_RESPONSE = {
    "message": "library_not_found",
    "details": "Library not found",
}, 404
USER_NOT_IN_FANS_RESPONSE = {
    "message": "user_not_in_fans",
    "details": "User not in fans",
}, 400
USER_ALREADY_EXISTS_RESPONSE = {
    "message": "user_already_exists",
    "details": "User already exists",
}, 401
USER_ID_NOT_PROVIDED_RESPONSE = {
    "message": "user_id_not_provided",
    "details": "User id not provided",
}, 404
AUTHOR_ID_NOT_PROVIDED_RESPONSE = {
    "message": "author_id_not_provided",
    "details": "Author id not provided",
}, 404
REGISTER_SUCCESSFUL_RESPONSE = {
    "message": "register_successful",
    "details": "Registered successfully",
}, 200
INSUFFICIENT_PERMISSIONS_RESPONSE = {
    "message": "insufficient_permissions",
    "details": "Insufficient permissions",
}, 404
OPINION_ALREADY_EXISTS_RESPONSE = {
    "message": "opinion_already_exists",
    "details": "Opinion already exists",
}, 400
BOOK_DOES_NOT_EXIST_RESPONSE = {
    "message": "book_does_not_exist",
    "details": "Book does not exist",
}, 404
OBJECT_NOT_FOUND_RESPONSE = {
    "message": "object_not_found",
    "details": "Object does not exist",
}, 404
PARAM_NOT_INT_RESPONSE = {
    "message": "param_not_int",
    "details": "Parameter is not an integer",
}, 400
OBJECT_CREATED_RESPONSE = {
    "message": "object_created",
    "details": "Object created",
}, 200
OBJECT_DELETED_RESPONSE = {
    "message": "object_deleted",
    "details": "Object deleted",
}, 200
OBJECT_MODIFIED_RESPONSE = {
    "message": "object_modified",
    "details": "Object modified",
}, 200
INVALID_PASSWORD_RESPONSE = {
    "message": "invalid_password",
    "details": "Invalid password",
}, 401
SORT_PARAM_DOES_NOT_EXIST = {
    "message": "sort_param_does_not_exist",
    "details": "Sort parameter does not exist",
}, 400
GENRES_RESPONSE = {
    "genres": [
        "Fantasy, Science fiction",
        "Thriller, Horror, Mystery and detective stories",
        "Young Adult",
        "Romance",
        "History",
        "Action & Adventure",
        "Biography",
        "Popular Science",
        "Children's",
        "Poetry, Plays",
        "Comic books",
        "Other",
    ]
}, 200

# Mutable
USERS_RESPONSE = {}, 200  # User model object/s
OPINIONS_RESPONSE = (
    {},
    200,
)  # Opinion model object/s
LIBRARIES_RESPONSE = {}, 200  # Library model object/s
BOOKS_RESPONSE = {}, 200  # Book model object/s
AUTHORS_RESPONSE = (
    {},
    200,
)  # Author model object/s
LOGGED_IN_USERS_RESPONSE = {}, 200  # { "email1": "token1", ... }
ALREADY_LOGGED_IN_RESPONSE = {
    "message": "already_logged_in",
    "details": "Already logged in",
    "token": "",  # Mutable str
}, 200
LOGIN_SUCCESSFUL_RESPONSE = {
    "message": "login_successful",
    "details": "Login successful",
    "token": "",  # Mutable str
}, 200

# BOOK_ANNOUNCEMENTS_LIST_RESPONSE = {}, 200
# BOOK_ANNOUNCEMENT_OBJECT_RESPONSE = {}, 200
