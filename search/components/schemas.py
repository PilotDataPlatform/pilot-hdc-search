# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from pydantic import BaseModel

from search.components.pagination import PageType


class BaseSchema(BaseModel):
    """Base class for all available schemas."""


class ListResponseSchema(BaseSchema):
    """Default schema for multiple base schemas in response."""

    num_of_pages: int
    page: int
    total: int
    result: list[BaseSchema]

    @classmethod
    def from_page(cls, page: PageType) -> 'ListResponseSchema':
        return cls(num_of_pages=page.total_pages, page=page.number, total=page.count, result=page.entries)
