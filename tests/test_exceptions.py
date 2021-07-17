"""Test Exceptions."""

from envalidate.exceptions import EnvError, EnvMissingError


def test_env_error_message():
    """Test EnvError Message."""
    expected = "invalid value."
    ex = EnvError(message=expected)
    assert ex.message == expected


def test_env_missing_env_name():
    """Test EnvMissingError Env Name."""
    expected = "key"
    ex = EnvMissingError(env_name=expected)
    assert ex.env_name == expected
