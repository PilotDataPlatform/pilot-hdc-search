# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

from pydantic import BaseModel

from search.components.types import StrEnum


class SortingOrder(StrEnum):
    """Available sorting orders."""

    ASC = 'asc'
    DESC = 'desc'


class Sorting(BaseModel):
    """Base sorting control parameters."""

    field: str | None = None
    order: SortingOrder

    def __bool__(self) -> bool:
        """Sorting considered valid when the field is specified."""

        return self.field is not None

    def apply(self) -> list[dict[str, Any]]:
        """Return sorting field with applied ordering that will be used as sort parameter."""

        return [{self.field: self.order.value}]
