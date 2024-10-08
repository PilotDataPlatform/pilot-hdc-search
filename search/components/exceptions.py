# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from abc import ABCMeta
from abc import abstractmethod
from http.client import INTERNAL_SERVER_ERROR
from http.client import UNPROCESSABLE_ENTITY
from typing import Sequence

from pydantic.error_wrappers import ErrorList


class ServiceException(Exception, metaclass=ABCMeta):
    """Base class for service exceptions."""

    domain: str = 'global'

    @property
    @abstractmethod
    def status(self) -> int:
        """HTTP status code applicable to the problem."""

        raise NotImplementedError

    @property
    @abstractmethod
    def code(self) -> str:
        """Component-specific error code."""

        raise NotImplementedError

    @property
    @abstractmethod
    def details(self) -> str:
        """Additional information with specific explanation for this occurrence of the problem."""

        raise NotImplementedError

    def dict(self) -> dict[str, str]:
        """Represent error as dictionary."""

        return {
            'code': f'{self.domain}.{self.code}',
            'details': self.details,
        }


class UnhandledException(ServiceException):
    """Raised when unhandled/unexpected internal error occurred."""

    @property
    def status(self) -> int:
        return INTERNAL_SERVER_ERROR

    @property
    def code(self) -> str:
        return 'unhandled_exception'

    @property
    def details(self) -> str:
        return 'Unexpected Internal Server Error'


class ServiceValidationError(ServiceException):
    """Raised when validation error is raised."""

    def __init__(self, errors: Sequence[ErrorList], *args, **kwargs) -> None:
        self.errors = errors

    @property
    def status(self) -> int:
        return UNPROCESSABLE_ENTITY

    @property
    def code(self) -> str:
        return 'validation_error'

    def dict(self) -> dict[str, str]:
        """Represent error as dictionary."""
        errors = []
        for error in self.errors:
            errors.append(
                {
                    'code': self.code,
                    'detail': error.get('msg'),
                    'source': error.get('loc'),
                }
            )

        return errors
