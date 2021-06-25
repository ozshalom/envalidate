"""Exceptions."""


class EnvError(EnvironmentError):
    """Env Error."""

    def __init__(self, message):
        """Init EnvError.

        :param message:
        """
        super().__init__(message)
        self.__message__ = message

    @property
    def message(self):
        """Message."""
        return self.__message__


class EnvMissingError(EnvError):
    """Env Missing Key Error."""

    def __init__(self, env_name: str) -> None:
        """Init EnvMissingError.

        :param env_name:
        """
        message = f"{env_name} : missing environment key"
        super().__init__(message)
