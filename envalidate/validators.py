"""Validators."""

from abc import ABC, abstractmethod
import json
import re
from typing import Any, Set
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from .exceptions import EnvError


class EnValidator(BaseModel, ABC):
    """Validator."""

    name: str = Field(description="validator name.", required=True)
    default: Any = Field(
        description="A fallback value, which will be present in the output if the env var wasn't"
        "specified. Providing a default effectively makes the env var optional."
        "Note that default values are not passed through validation logic",
        required=False,
        default=None,
    )
    choices: Set = Field(
        description="An Array that lists the admissible parsed values for the env var.",
        required=False,
        default=None,
    )
    desc: str = Field(
        description="A string that describes the env var",
        required=False,
        default=None,
    )
    example: str = Field(
        description="An example value for the env var.",
        required=False,
        default=None,
    )
    docs: str = Field(
        description="A url that leads to more detailed documentation about the env var.",
        required=False,
        default=None,
    )

    def envalidate(self, value: str) -> Any:
        """Valid key and raise error if invalid or return value if valid."""
        valid_value = self.__validate__value__(value)
        if self.choices and valid_value not in self.choices:
            raise EnvError(
                self.format_validator_desc(
                    f"Invalid {self.name} input: {value}, not in [{self.choices}]"
                )
            )
        return valid_value

    @abstractmethod
    def __validate__value__(self, value) -> Any:
        """Validate Value."""

    def format_validator_desc(self, message) -> str:
        """Format validator description."""
        example = f"eg. {self.example}" if self.example else ""
        docs = f"See. {self.docs}" if self.docs else ""
        desc = self.desc or ""
        return f"{message} [{desc} {example} {docs}]".strip()


class Str(EnValidator):
    """Passes string values through.

    will ensure an value is present unless a default value is given.
    Note that an empty string is considered a valid value
    """

    def __init__(self, **kwargs):
        """Init Str Validator."""
        super().__init__(name="str", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate str value."""
        return value


class Bool(EnValidator):
    """Parses env var strings "1", "0", "True", "False" into booleans."""

    def __init__(self, **kwargs):
        """Init Bool Validator."""
        super().__init__(name="bool", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate bool value."""
        if value == "0" or value.lower() == "false":
            return False
        if value == "1" or value.lower() == "true":
            return True
        raise EnvError(self.format_validator_desc(f"Invalid {self.name} input: {value}"))


class Number(EnValidator):
    """Parses an env var (eg. "42", "0.23", "1e5") into a Number."""

    def __init__(self, **kwargs):
        """Init Number Validator."""
        super().__init__(name="number", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate number value."""
        try:
            value = float(value)
            return int(value) if float.is_integer(value) else value
        except ValueError as ex:
            raise EnvError(
                self.format_validator_desc(f"Invalid {self.name} input: {value}")
            ) from ex


class RegexEnValidator(EnValidator):
    """Ensures an env var match regex pattern."""

    pattern: str = Field(required=True)

    def __init__(self, name, **kwargs):
        """Init Regex Validator."""
        super().__init__(name=name, **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate regex value."""
        match = re.search(re.compile(self.pattern), value)
        if match:
            return value
        raise EnvError(self.format_validator_desc(f"Invalid {self.name} input: {value}"))


class Email(RegexEnValidator):
    """Ensures an env var is an email address."""

    def __init__(self, **kwargs):
        """Init Email Validator."""
        email_regex = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        super().__init__(name="e-mail", pattern=email_regex, **kwargs)


class IPAddress(RegexEnValidator):
    """Ensures an env var is an ip address with or without port."""

    def __init__(self, **kwargs):
        """Init IP Validator."""
        ipv4_regex = r"[0-9]+(?:\.[0-9]+){3}(:[0-9]+)?"
        super().__init__(name="ip address", pattern=ipv4_regex, **kwargs)


class Port(EnValidator):
    """Ensures an env var is a TCP port (1-65535)."""

    def __init__(self, **kwargs):
        """Init Port Validator."""
        super().__init__(name="port", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate port value."""
        try:
            value = float(value)
            if float.is_integer(value) and 1 <= value <= 65535:
                return int(value)
        except ValueError:
            ...

        raise EnvError(self.format_validator_desc(f"Invalid {self.name} input: {value}"))


class Url(EnValidator):
    """Ensures an env var is a url with a protocol and hostname."""

    def __init__(self, **kwargs):
        """Init Url Validator."""
        super().__init__(name="url", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate url value."""
        result = urlparse(value)
        if result.scheme and result.netloc:
            return value
        raise EnvError(self.format_validator_desc(f"Invalid {self.name} input: {value}"))


class Json(EnValidator):
    """Parses an env var with JSON.parse."""

    def __init__(self, **kwargs):
        """Init Json Validator."""
        super().__init__(name="json", **kwargs)

    def __validate__value__(self, value) -> Any:
        """Validate json value."""
        try:
            value = json.loads(value)
            return value
        except json.decoder.JSONDecodeError as ex:
            raise EnvError(
                self.format_validator_desc(f"Invalid {self.name} input: {value}")
            ) from ex
