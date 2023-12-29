from abc import ABC, abstractmethod
from sql import SQLite, DATABASENAME


class UserState(ABC):
    @abstractmethod
    def login(self, user):
        pass

    def logout(self, user):
        pass

    def __str__(self) -> str:
        pass


class LoggedInState(UserState):
    def login(self, user):
        raise Exception("Already logged in, log out to do this.")

    def logout(self, user):
        user.state = LoggedOutState()

    def __str__(self) -> str:
        return "Logged in."


class LoggedOutState(UserState):
    def login(self, user):
        if not user.user_exists():
            raise Exception(f"User with username {user.username} not found. "
                            "Create a user with a username first.")
        user.state = LoggedInState()

    def logout(self, user):
        raise Exception("Already logged out, log out to do this")

    def __str__(self) -> str:
        return "Logged out."


class User:
    def __init__(self,
                 username: str | None = None,
                 ) -> None:
        self.username = "admin"

        self.state = LoggedOutState()

    def login(self) -> None:
        self.state.login(self)

    def logout(self) -> None:
        self.state.logout(self)

    def user_exists(self) -> bool:
        with SQLite(DATABASENAME) as db:
            user_row = db.cursor.execute("SELECT username FROM user WHERE username = ?",
                                         (self.username,)).fetchone()
            return bool(user_row)

