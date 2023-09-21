# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from faker import Faker

from search.components.crud import CRUD


class BaseFactory:
    """Base class for creating testing purpose entries."""

    crud: CRUD
    fake: Faker

    def __init__(self, crud: CRUD, fake: Faker) -> None:
        self.crud = crud
        self.fake = fake

    async def create_index(self) -> None:
        """Create a new index."""

        await self.crud.create_index()

    async def delete_index(self) -> None:
        """Remove an existing index."""

        await self.crud.client.indices.delete(index=self.crud.index)
