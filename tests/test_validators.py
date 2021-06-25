"""Test Validators."""

import pytest
from pytest_lazyfixture import lazy_fixture

from envalidate import Bool, Email, EnValidator, IPAddress, Json, Number, Port, Str, Url
from envalidate.exceptions import EnvError


@pytest.mark.parametrize(
    "validator, value, expected",
    [
        pytest.param(
            lazy_fixture("number_validator_with_choices"),
            1,
            1,
            marks=pytest.mark.parametrize,
            id="Choice - 1",
        ),
        pytest.param(
            lazy_fixture("str_validator_with_choices"),
            "A",
            "A",
            marks=pytest.mark.parametrize,
            id="Choice - A",
        ),
        pytest.param(
            lazy_fixture("str_validator"),
            None,
            "None",
            marks=pytest.mark.parametrize,
            id="Str Validator : None",
        ),
        pytest.param(
            lazy_fixture("str_validator"),
            1,
            "1",
            marks=pytest.mark.parametrize,
            id="Str Validator : 1",
        ),
        pytest.param(
            lazy_fixture("str_validator"),
            False,
            "False",
            marks=pytest.mark.parametrize,
            id="Str Validator : False",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            0,
            False,
            marks=pytest.mark.parametrize,
            id="Bool Validator : 0=False",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            1,
            True,
            marks=pytest.mark.parametrize,
            id="Bool Validator : 1=True",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "False",
            False,
            marks=pytest.mark.parametrize,
            id="Bool Validator : False=False",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "false",
            False,
            marks=pytest.mark.parametrize,
            id="Bool Validator : false=False",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "True",
            True,
            marks=pytest.mark.parametrize,
            id="Bool Validator : True=True",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "true",
            True,
            marks=pytest.mark.parametrize,
            id="Bool Validator : true=True",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            1,
            1,
            marks=pytest.mark.parametrize,
            id="Number Validator : 1 (int)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            1.0,
            1.0,
            marks=pytest.mark.parametrize,
            id="Number Validator : 1 (float)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            0x10,
            16,
            marks=pytest.mark.parametrize,
            id="Number Validator : 0x10=16 (Hex)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            1e5,
            1e5,
            marks=pytest.mark.parametrize,
            id="Number Validator : 1e5",
        ),
        pytest.param(
            lazy_fixture("email_validator"),
            "test@gmail.com",
            "test@gmail.com",
            marks=pytest.mark.parametrize,
            id="Email Validator : test@gmail.com",
        ),
        pytest.param(
            lazy_fixture("email_validator"),
            "test@gmail.co.il",
            "test@gmail.co.il",
            marks=pytest.mark.parametrize,
            id="Email Validator : test@gmail.co.il",
        ),
        pytest.param(
            lazy_fixture("ip_validator"),
            "192.168.0.1",
            "192.168.0.1",
            marks=pytest.mark.parametrize,
            id="Host Validator : 192.168.0.1 (ip)",
        ),
        pytest.param(
            lazy_fixture("ip_validator"),
            "192.168.0.1:8000",
            "192.168.0.1:8000",
            marks=pytest.mark.parametrize,
            id="IP Validator : 192.168.0.1:8000 (ip:port)",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            8000,
            8000,
            marks=pytest.mark.parametrize,
            id="Port Validator : 8000",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            1,
            1,
            marks=pytest.mark.parametrize,
            id="Port Validator : 1",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            65535,
            65535,
            marks=pytest.mark.parametrize,
            id="Port Validator : 65535",
        ),
        pytest.param(
            lazy_fixture("url_validator"),
            "https://www.test.com",
            "https://www.test.com",
            marks=pytest.mark.parametrize,
            id="Url Validator : https://www.test.com",
        ),
        pytest.param(
            lazy_fixture("json_validator"),
            '{"x" : "test"}',
            {"x": "test"},
            marks=pytest.mark.parametrize,
            id='Json Validator : {"x" : "test"}',
        ),
        pytest.param(
            lazy_fixture("json_validator"),
            '[{"x" : "test"}, {"x" : "test2"}]',
            [{"x": "test"}, {"x": "test2"}],
            marks=pytest.mark.parametrize,
            id='Json Validator : [{"x" : "test"}, {"x" : "test2"}]',
        ),
    ],
)
def test_validators_valid(monkeypatch, validator: EnValidator, value, expected):
    """Test validator valid value.

    :param monkeypatch:
    :param validator:
    :param value:
    :param expected:
    :return:
    """
    key = "TEST_KEY"
    raw_value = str(value)
    monkeypatch.setenv(key, raw_value)
    actual = validator.envalidate(raw_value)
    assert actual == expected


@pytest.mark.parametrize(
    "validator, value",
    [
        pytest.param(
            lazy_fixture("number_validator_with_choices"),
            0,
            marks=pytest.mark.parametrize,
            id="Choice - 0 not in choices",
        ),
        pytest.param(
            lazy_fixture("str_validator_with_choices"),
            "Z",
            marks=pytest.mark.parametrize,
            id="Choice - Z not in choices",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            22,
            marks=pytest.mark.parametrize,
            id="Bool Validator : 22 (number)",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "t",
            marks=pytest.mark.parametrize,
            id="Bool Validator : t (str)",
        ),
        pytest.param(
            lazy_fixture("bool_validator"),
            "t",
            marks=pytest.mark.parametrize,
            id="Bool Validator : f (str)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            "abc",
            marks=pytest.mark.parametrize,
            id="Number Validator : abc (str)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            "192.168.0.1",
            marks=pytest.mark.parametrize,
            id="Number Validator : 192.168.0.1 (IP)",
        ),
        pytest.param(
            lazy_fixture("number_validator"),
            True,
            marks=pytest.mark.parametrize,
            id="Number Validator : True (bool)",
        ),
        pytest.param(
            lazy_fixture("email_validator"),
            "test.gmail.com",
            marks=pytest.mark.parametrize,
            id="Email Validator : test.gmail.com",
        ),
        pytest.param(
            lazy_fixture("email_validator"),
            "test@gmail@com",
            marks=pytest.mark.parametrize,
            id="Email Validator : test@gmail@com",
        ),
        pytest.param(
            lazy_fixture("ip_validator"),
            "192.168.0",
            marks=pytest.mark.parametrize,
            id="IP Validator : 192.168.0 (ip 3)",
        ),
        pytest.param(
            lazy_fixture("ip_validator"),
            "192.168.0:8000",
            marks=pytest.mark.parametrize,
            id="IP Validator : 192.168.0:8000 (ip:port)",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            65536,
            marks=pytest.mark.parametrize,
            id="Port Validator : 65536 (over max)",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            0,
            marks=pytest.mark.parametrize,
            id="Port Validator : 0 (below min)",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            -8000,
            marks=pytest.mark.parametrize,
            id="Port Validator : -8000 (negative)",
        ),
        pytest.param(
            lazy_fixture("port_validator"),
            800.9,
            marks=pytest.mark.parametrize,
            id="Port Validator : 800.9 (float)",
        ),
        pytest.param(
            lazy_fixture("url_validator"),
            None,
            marks=pytest.mark.parametrize,
            id="Url Validator : None",
        ),
        pytest.param(
            lazy_fixture("url_validator"),
            "test",
            marks=pytest.mark.parametrize,
            id="Url Validator : test",
        ),
        pytest.param(
            lazy_fixture("url_validator"),
            "www.test.com",
            marks=pytest.mark.parametrize,
            id="Url Validator : no schema",
        ),
        pytest.param(
            lazy_fixture("url_validator"),
            "https://",
            marks=pytest.mark.parametrize,
            id="Url Validator : no netloc",
        ),
        pytest.param(
            lazy_fixture("json_validator"),
            "{'x': 1}",
            marks=pytest.mark.parametrize,
            id="Json Validator : no double quotes",
        ),
        pytest.param(
            lazy_fixture("json_validator"),
            '{"x": 1',
            marks=pytest.mark.parametrize,
            id="Json Validator : wrong syntax",
        ),
    ],
)
def test_validators_invalid(monkeypatch, validator: EnValidator, value):
    """Test validator invalid value.

    :param monkeypatch:
    :param validator:
    :param value:
    :return:
    """
    key = "TEST_KEY"
    raw_value = str(value)
    monkeypatch.setenv(key, raw_value)
    with pytest.raises(EnvError):
        validator.envalidate(raw_value)


@pytest.mark.parametrize(
    "validator, default, choices, desc, example, docs",
    [
        pytest.param(
            Str(default="A", choices={"A", "B"}, desc="str", example="A", docs="str"),
            "A",
            {"A", "B"},
            "str",
            "A",
            "str",
            marks=pytest.mark.parametrize,
            id="Str",
        ),
        pytest.param(
            Number(default=1, choices={1, 2, 3.0}, desc="number", example="1", docs="number"),
            1,
            {1, 2, 3.0},
            "number",
            "1",
            "number",
            marks=pytest.mark.parametrize,
            id="Number",
        ),
        pytest.param(
            Bool(default=True, choices={True, False}, desc="bool", example="True", docs="bool"),
            True,
            {True, False},
            "bool",
            "True",
            "bool",
            marks=pytest.mark.parametrize,
            id="Bool",
        ),
        pytest.param(
            Email(
                default=None,
                choices={"test@google.com", "tese2@google.com"},
                desc="email",
                example="test@google.com",
                docs="email",
            ),
            None,
            {"test@google.com", "tese2@google.com"},
            "email",
            "test@google.com",
            "email",
            marks=pytest.mark.parametrize,
            id="Email",
        ),
        pytest.param(
            IPAddress(
                default="192.168.0.1",
                choices={"192.168.0.1", "192.168.0.2"},
                desc="ip",
                example="192.168.0.1",
                docs="ip",
            ),
            "192.168.0.1",
            {"192.168.0.1", "192.168.0.2"},
            "ip",
            "192.168.0.1",
            "ip",
            marks=pytest.mark.parametrize,
            id="IPAddress",
        ),
        pytest.param(
            Port(
                default=8000,
                choices={8001, 8002},
                desc="port",
                example="8000",
                docs="port",
            ),
            8000,
            {8001, 8002},
            "port",
            "8000",
            "port",
            marks=pytest.mark.parametrize,
            id="Port",
        ),
        pytest.param(
            Url(
                default="www.test.com",
                choices={"www.test.com", "https://www.test.com"},
                desc="url",
                example="www.test.com",
                docs="url",
            ),
            "www.test.com",
            {"www.test.com", "https://www.test.com"},
            "url",
            "www.test.com",
            "url",
            marks=pytest.mark.parametrize,
            id="Url",
        ),
        pytest.param(
            Json(
                default=None,
                choices=None,
                desc="json",
                example='{"x": 1}',
                docs="json",
            ),
            None,
            None,
            "json",
            '{"x": 1}',
            "json",
            marks=pytest.mark.parametrize,
            id="json",
        ),
    ],
)
def test_validator_params(validator: EnValidator, default, choices, desc, example, docs):
    """Test validator params."""
    assert validator.default == default
    assert validator.choices == choices
    assert validator.desc == desc
    assert validator.example == example
    assert validator.docs == docs
