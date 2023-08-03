class User:
    def __init__(self, email, password):
        self.email = email
        self.password = self.set_password(password)
        self.role = 'user'

    def set_password(self, password):
        # Hash password here
        return password


def test_new_user():
    """
    GIVEN
    WHEN
    THEN
    """
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password == 'FlaskIsAwesome'
    assert user.role == 'user'
