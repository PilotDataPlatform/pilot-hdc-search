# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from pydantic import BaseModel

from search.components.search_query import SearchQuery


class Filtering(BaseModel):
    """Base filtering control parameters."""

    def __bool__(self) -> bool:
        """Filtering considered valid when at least one attribute has a value."""

        values = self.dict()

        for name in self.__fields__.keys():
            if values[name] is not None:
                return True

        return False

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        raise NotImplementedError
