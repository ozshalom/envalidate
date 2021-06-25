"""Test Reporters."""

from unittest.mock import call

import pytest
from pytest_lazyfixture import lazy_fixture

from envalidate.exceptions import EnvError, EnvMissingError


@pytest.mark.parametrize(
    "reporter, errors",
    [
        pytest.param(
            lazy_fixture("default_reporter"),
            {"HOST": EnvMissingError("HOST"), "PORT": EnvError("Invalid value")},
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
        pytest.param(
            lazy_fixture("default_reporter"),
            {"HOST": EnvMissingError("HOST")},
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
        pytest.param(
            lazy_fixture("default_reporter"),
            {"PORT": EnvError("Invalid value")},
            marks=pytest.mark.parametrize,
            id="os.environ",
        ),
    ],
)
def test_errors(reporter, errors):
    """Test missing errors."""
    reporter.report(errors)
    assert reporter.__on_error__.call_count == 1
    assert reporter.__on_error__.call_args == call(errors)
