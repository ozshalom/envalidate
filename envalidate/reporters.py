"""Reporters."""

from abc import ABC, abstractmethod
import logging
from typing import Callable, Dict, List

from .exceptions import EnvError, EnvMissingError


class Reporter(ABC):
    """Reporter."""

    def __init__(
        self,
        logger=None,
        on_error: Callable[[Dict[str, EnvError]], None] = None,
    ):
        """Class handling errors and console output.

        :param logger:
        :param on_error:
        """
        self.__logger__ = (
            logger
            if logger
            else logging.getLogger(
                f"{__name__}.{self.__class__.__name__}",
            )
        )
        self.__on_error__ = on_error

    @abstractmethod
    def report(self, errors: Dict[str, EnvError]):
        """Create report.

        :param errors:
        """


class DefaultReporter(Reporter):
    """Default Reporter.

    logger = __name__.__class__.__name__
    """

    def __init__(self, on_error: Callable[[Dict[str, EnvError]], None] = None):
        """Init DefaultReporter."""
        super().__init__(on_error=on_error)

    def report(self, errors: Dict[str, EnvError]):
        """Create report, using logger.

        :param errors:
        """
        if not errors:
            return

        rule = "=" * 100
        missing_vars: List[str] = []
        invalid_vars: List[str] = []
        for key, error in errors.items():
            if isinstance(error, EnvMissingError):
                missing_vars.append(f"\t{key}: {error.message} (required)")
            else:
                invalid_vars.append(f"\t{key}: {error.message} (invalid format)")
        if missing_vars:
            missing_vars.insert(0, "Missing environment variables:")
        if invalid_vars:
            invalid_vars.insert(0, "Invalid environment variables:")
        output = "\n".join([rule, "\n".join(invalid_vars), "\n".join(missing_vars), rule])

        self.__logger__.error(output)

        if self.__on_error__:
            self.__on_error__(errors)
        else:
            raise TypeError("Environment validation failed")
