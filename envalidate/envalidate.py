"""Main Envalidate."""

from typing import Any, Dict

from pydantic import BaseModel, create_model

from .exceptions import EnvError, EnvMissingError
from .reporters import DefaultReporter, Reporter
from .validators import EnValidator

DEFAULT_REPORTER = DefaultReporter()


class FrozenModel(BaseModel):
    """Frozen Model."""

    @classmethod
    def with_fields(cls, model_name, **field_definitions):
        """Create FrozenModel with dynamic fields."""
        return create_model(model_name, __base__=cls, **field_definitions)

    class Config:
        """Config."""

        allow_mutation = False
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


def read_env(
    environment, validators: Dict[str, EnValidator], reporter: Reporter = DEFAULT_REPORTER
):
    """Returns a sanitized, immutable environment object, and accepts three positional arguments.

    :param environment: An object containing your env vars (eg. os.environ)
    :param validators: An object that specifies the format of required vars.
    :param reporter: Pass in a function to override the default error handling and console output.
    See reporters.py for the default implementation
    :return: By default, will log an error message and
    throw TypeError if any required env vars are missing or invalid.
    if all env are validated then Frozen CleanEnv will return.
    """

    def read_key(_key, _validator, _environment) -> str:
        """Read key value from environment."""
        if _key not in _environment and not _validator.default:
            raise EnvMissingError(_key)
        return environment.get(_key, _validator.default)

    def create_frozen_model(values: Dict[str, Any]):
        """Create frozen model."""
        fields = {k: (type(v), ...) for k, v in values.items()}
        env_model = FrozenModel.with_fields("CleanEnv", **fields)
        return env_model(**values)

    cleaned_env: Dict[str, Any] = {}
    errors: Dict[str, EnvError] = {}
    for key, envalidator in validators.items():
        try:
            value = read_key(key, envalidator, environment)
            valid_value = envalidator.envalidate(value)
            cleaned_env[key] = valid_value
        except (EnvError, EnvMissingError) as ex:
            errors[key] = ex
    reporter.report(errors)

    return create_frozen_model(cleaned_env)
