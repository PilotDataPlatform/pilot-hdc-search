# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import random
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

import pytest

from search.components import DatasetActivity
from search.components import ModelList
from search.components.dataset_activity.crud import DatasetActivityCRUD
from search.components.dataset_activity.models import DatasetActivityType
from search.components.dataset_activity.schemas import DatasetActivityCreateSchema
from tests.fixtures.components._base_factory import BaseFactory


class DatasetActivityFactory(BaseFactory):
    """Create dataset activity related entries for testing purposes."""

    def generate(
        self,
        activity_type: DatasetActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str | None = ...,
        target_name: str | None = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
        network_origin: str = ...,
    ) -> DatasetActivityCreateSchema:

        if activity_type is ...:
            activity_type = random.choice(DatasetActivityType.values())

        if activity_time is ...:
            activity_time = self.fake.past_datetime_utc()

        if container_code is ...:
            container_code = self.fake.unique.word().lower() + self.fake.unique.word().lower()

        if version is ...:
            version = f'{self.fake.pyint(0, 4)}.{self.fake.pyint(0, 20)}'

        if target_name is ...:
            target_name = '.'.join(self.fake.words(3)).lower()

        if user is ...:
            user = f'{self.fake.pystr()}_{self.fake.first_name()}'.lower()

        if changes is ...:
            changes = []

        if network_origin is ...:
            network_origin = 'unknown'

        return DatasetActivityCreateSchema(
            activity_type=activity_type,
            activity_time=activity_time,
            container_code=container_code,
            version=version,
            target_name=target_name,
            user=user,
            changes=changes,
            network_origin=network_origin,
        )

    async def create(
        self,
        activity_type: DatasetActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str | None = ...,
        target_name: str | None = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
        network_origin: str = ...,
        **kwds: Any,
    ) -> DatasetActivity:
        entry = self.generate(
            activity_type,
            activity_time,
            container_code,
            version,
            target_name,
            user,
            changes,
            network_origin,
        )

        # Make the document immediately appear in search results
        # https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-refresh.html#docs-refresh
        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def bulk_create(
        self,
        number: int,
        activity_type: DatasetActivityType = ...,
        activity_time: datetime = ...,
        container_code: str = ...,
        version: str | None = ...,
        target_name: str | None = ...,
        user: str = ...,
        changes: list[dict[str, Any]] = ...,
        network_origin: str = ...,
        **kwds: Any,
    ) -> ModelList[DatasetActivity]:
        return ModelList(
            [
                await self.create(
                    activity_type,
                    activity_time,
                    container_code,
                    version,
                    target_name,
                    user,
                    changes,
                    network_origin,
                    **kwds,
                )
                for _ in range(number)
            ]
        )


@pytest.fixture
def dataset_activity_crud(es_client) -> DatasetActivityCRUD:
    return DatasetActivityCRUD(es_client)


@pytest.fixture
async def dataset_activity_factory(dataset_activity_crud, fake) -> AsyncGenerator[DatasetActivityFactory]:
    dataset_activity_factory = DatasetActivityFactory(dataset_activity_crud, fake)

    await dataset_activity_factory.create_index()
    yield dataset_activity_factory
    await dataset_activity_factory.delete_index()
