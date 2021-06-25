"""Test CleanEnv."""
import os
from unittest.mock import Mock

import pytest

from envalidate import read_env, Str
from envalidate.reporters import DefaultReporter, Reporter


def test_envalid_with_errors(set_invalid_values, default_validators):
    """Test Envalidate with errors no reporter."""
    with pytest.raises(TypeError):
        read_env(environment=os.environ, validators=default_validators)


def test_envalid_with_errors_with_reporter(set_invalid_values, default_validators):
    """Test Envalidate with errors and reporter."""
    on_error_mock = Mock()
    reporter = DefaultReporter(on_error=on_error_mock)
    read_env(environment=os.environ, validators=default_validators, reporter=reporter)
    assert on_error_mock.call_count == 1


@pytest.mark.parametrize(
    "environment",
    [
        pytest.param(
            os.environ,
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
    ],
)
def test_read_env(monkeypatch, environment, default_validators):
    """Test read env."""
    monkeypatch.setenv("HOST", "google")
    monkeypatch.setenv("IP", "192.168.0.1")
    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("IS_TEST", "True")
    monkeypatch.setenv("EMAIL", "test@gmail.com")
    monkeypatch.setenv("HOME_PAGE", "https://www.google.com")
    monkeypatch.setenv("CONFIG", '{"concurrency": 20}')
    monkeypatch.setenv("AGENTS", "4")

    env = read_env(environment, default_validators)
    assert env.HOST == "google"
    assert env.IP == "192.168.0.1"
    assert env.PORT == 8000
    assert env.IS_TEST is True
    assert env.EMAIL == "test@gmail.com"
    assert env.HOME_PAGE == "https://www.google.com"
    assert env.CONFIG == {"concurrency": 20}
    assert env.AGENTS == 4


@pytest.mark.parametrize(
    "environment, reporter",
    [
        pytest.param(
            os.environ,
            DefaultReporter(),
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
    ],
)
def test_read_env_with_reporter(monkeypatch, environment, reporter: Reporter):
    """Test read env with reporter."""
    spec = {"HOST": Str()}
    monkeypatch.setenv("HOST", "google")

    env = read_env(environment, spec, reporter)
    assert env.HOST == "google"


@pytest.mark.parametrize(
    "environment",
    [
        pytest.param(
            os.environ,
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
    ],
)
def test_read_env_failed_set_attribute(monkeypatch, environment):
    """Test read env, trying to set attribute."""
    spec = {"HOST": Str()}
    monkeypatch.setenv("HOST", "google")

    env = read_env(environment, spec)
    with pytest.raises(TypeError):
        env.HOST = "yahoo"
