# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import math
from typing import TypeVar

from pydantic import BaseModel
from pydantic import conint

from search.components.models import Model


class Pagination(BaseModel):
    """Base pagination control parameters."""

    page: conint(ge=1) = 1
    page_size: conint(ge=1) = 20

    @property
    def size(self) -> int:
        return self.page_size

    @property
    def from_(self) -> int:
        return self.page_size * (self.page - 1)


class Page(BaseModel):
    """Represent one page of the response."""

    pagination: Pagination
    count: int
    entries: list[Model]

    @property
    def number(self) -> int:
        return self.pagination.page

    @property
    def total_pages(self) -> int:
        return math.ceil(self.count / self.pagination.page_size)


PageType = TypeVar('PageType', bound=Page)
