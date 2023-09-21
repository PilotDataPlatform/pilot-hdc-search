# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import random
from datetime import datetime
from typing import Any
from uuid import UUID

import pytest

from search.components import ItemActivity
from search.components import ModelList
from search.components.item_activity.crud import ItemActivityCRUD
from search.components.item_activity.models import ItemActivityType
from search.components.item_activity.schemas import ItemActivityCreateSchema
from search.components.models import ContainerType
from tests.fixtures.components._base_factory import BaseFactory


class ItemActivityFactory(BaseFactory):
    """Create item activity related entries for testing purposes."""

    def generate(  # noqa: C901
        self,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        item_id: UUID | None = ...,
        item_type: str = ...,
        item_name: str = ...,
        item_parent_path: str = ...,
        zone: int = ...,
        user: str = ...,
        imported_from: str | None = ...,
        changes: list[dict[str, Any]] = ...,
    ) -> ItemActivityCreateSchema:
        if activity_type is ...:
            activity_type = random.choice(ItemActivityType.values())

        if activity_time is ...:
            activity_time = self.fake.past_datetime_utc()

        if container_code is ...:
            container_code = self.fake.word().lower()

        if container_type is ...:
            container_type = ContainerType.PROJECT

        if item_id is ...:
            item_id = self.fake.uuid4(None)

        if item_type is ...:
            item_type = self.fake.word().lower()

        if item_name is ...:
            item_name = self.fake.word().lower()

        if item_parent_path is ...:
            item_parent_path = self.fake.file_path(depth=2)

        if zone is ...:
            zone = self.fake.pyint(0, 100)

        if user is ...:
            user = self.fake.word().lower()

        if imported_from is ...:
            imported_from = self.fake.word().lower()

        if changes is ...:
            changes = []

        return ItemActivityCreateSchema(
            activity_type=activity_type,
            activity_time=activity_time,
            container_code=container_code,
            container_type=container_type,
            item_id=item_id,
            item_type=item_type,
            item_name=item_name,
            item_parent_path=item_parent_path,
            zone=zone,
            user=user,
            imported_from=imported_from,
            changes=changes,
        )

    async def create(
        self,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        item_id: UUID | None = ...,
        item_type: str = ...,
        item_name: str = ...,
        item_parent_path: str = ...,
        zone: int = ...,
        user: str = ...,
        imported_from: str | None = ...,
        changes: list[dict[str, Any]] = ...,
        **kwds: Any,
    ) -> ItemActivity:
        entry = self.generate(
            activity_type,
            activity_time,
            container_code,
            container_type,
            item_id,
            item_type,
            item_name,
            item_parent_path,
            zone,
            user,
            imported_from,
            changes,
        )

        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def bulk_create(
        self,
        number: int,
        activity_type: ItemActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        item_id: UUID | None = ...,
        item_type: str = ...,
        item_name: str = ...,
        item_parent_path: str = ...,
        zone: int = ...,
        user: str = ...,
        imported_from: str | None = ...,
        changes: list[dict[str, Any]] = ...,
        **kwds: Any,
    ) -> ModelList[ItemActivity]:
        return ModelList(
            [
                await self.create(
                    activity_type,
                    activity_time,
                    container_code,
                    container_type,
                    item_id,
                    item_type,
                    item_name,
                    item_parent_path,
                    zone,
                    user,
                    imported_from,
                    changes,
                    **kwds,
                )
                for _ in range(number)
            ]
        )


@pytest.fixture
def item_activity_crud(es_client) -> ItemActivityCRUD:
    yield ItemActivityCRUD(es_client)


@pytest.fixture
async def item_activity_factory(item_activity_crud, fake) -> ItemActivityFactory:
    item_activity_factory = ItemActivityFactory(item_activity_crud, fake)

    await item_activity_factory.create_index()
    yield item_activity_factory
    await item_activity_factory.delete_index()
