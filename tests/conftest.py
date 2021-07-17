"""Fixtures."""
from typing import Callable, Dict, Set
from unittest.mock import Mock

import pytest

from envalidate import Bool, Email, IPAddress, Json, Number, Port, Str, Url
from envalidate.exceptions import EnvError
from envalidate.reporters import DefaultReporter, Reporter


@pytest.fixture(scope="session")
def str_validator():
    """Str validator."""
    yield Str()


@pytest.fixture(scope="session")
def bool_validator():
    """Bool validator."""
    yield Bool()


@pytest.fixture(scope="session")
def number_validator():
    """Number validator."""
    yield Number()


@pytest.fixture(scope="session")
def email_validator():
    """Email validator."""
    yield Email()


@pytest.fixture(scope="session")
def ip_validator():
    """IP validator."""
    yield IPAddress()


@pytest.fixture(scope="session")
def port_validator():
    """Port validator."""
    yield Port()


@pytest.fixture(scope="session")
def url_validator():
    """Url validator."""
    yield Url()


@pytest.fixture(scope="session")
def json_validator():
    """Json validator."""
    yield Json()


@pytest.fixture(scope="session")
def str_choices() -> Set:
    """Str Choices."""
    return {"A", "B"}


@pytest.fixture(scope="session")
def number_choices() -> Set:
    """Number Choices."""
    return {1, 2, 3.7}


@pytest.fixture(scope="session")
def str_validator_with_choices(str_choices):
    """Str Validator With Choices."""
    yield Str(choices=str_choices)


@pytest.fixture(scope="session")
def number_validator_with_choices(number_choices):
    """Number Validator With Choices."""
    yield Number(choices=number_choices)


@pytest.fixture()
def default_reporter() -> Reporter:
    """DefaultReporter."""
    mock_error = Mock(spec=Callable[[Dict[str, EnvError]], None])
    yield DefaultReporter(on_error=mock_error)


@pytest.fixture(scope="session")
def default_validators():
    """Return default validators."""
    return {
        "HOST": Str(),
        "IP": IPAddress(),
        "PORT": Port(),
        "IS_TEST": Bool(),
        "EMAIL": Email(),
        "HOME_PAGE": Url(),
        "CONFIG": Json(),
        "AGENTS": Number(),
    }


@pytest.fixture()
def set_invalid_values(monkeypatch):
    """Set Invalid values."""
    monkeypatch.setenv("IP", "1")
    monkeypatch.setenv("PORT", "8000A")
    monkeypatch.setenv("IS_TEST", "t")
    monkeypatch.setenv("EMAIL", "test_gmail.com")
    monkeypatch.setenv("HOME_PAGE", "://www.google.com")
    monkeypatch.setenv("CONFIG", '{"concurrency"= 20}')
    monkeypatch.setenv("AGENTS", "4A")
