# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import random
from datetime import datetime
from typing import Any
from uuid import UUID

import pytest

from search.components import MetadataItem
from search.components import ModelList
from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.models import MetadataItemStatus
from search.components.metadata_item.models import MetadataItemType
from search.components.metadata_item.schemas import MetadataItemCreateSchema
from search.components.models import ContainerType
from tests.fixtures.components._base_factory import BaseFactory


class MetadataItemFactory(BaseFactory):
    """Create metadata item related entries for testing purposes."""

    def generate(  # noqa: C901
        self,
        id_: UUID = ...,
        parent: UUID | None = ...,
        parent_path: str | None = ...,
        type_: MetadataItemType = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_id: UUID | None = ...,
        template_name: str | None = ...,
        attributes: dict[str, Any] | None = ...,
        archived: bool = ...,
    ) -> MetadataItemCreateSchema:
        if id_ is ...:
            id_ = self.fake.uuid4(None)

        if parent is ...:
            parent = random.choice([None, self.fake.uuid4(None)])

        if parent_path is ...:
            parent_path = '.'.join(self.fake.words(4)).lower()
            if parent is None:
                parent_path = None

        if type_ is ...:
            type_ = random.choice(MetadataItemType.values())

        is_folder_type = type_ in (MetadataItemType.FOLDER, MetadataItemType.NAME_FOLDER)

        if zone is ...:
            zone = self.generate_zone()

        if name is ...:
            name = self.fake.unique.file_name().lower()
            if is_folder_type:
                name = self.fake.unique.word().lower()

        if size is ...:
            size = self.generate_size()
            if is_folder_type:
                size = 0

        if owner is ...:
            owner = self.generate_owner()

        if container_code is ...:
            container_code = self.generate_container_code()

        if container_type is ...:
            container_type = ContainerType.PROJECT

        if created_time is ...:
            created_time = self.fake.past_datetime_utc()

        if last_updated_time is ...:
            last_updated_time = self.fake.past_datetime_utc()

        if tags is ...:
            tags = self.fake.words(3, unique=True)

        if template_id is ...:
            template_id = self.fake.uuid4(None)

        if template_name is ...:
            template_name = self.fake.word().lower()

        if attributes is ...:
            attributes = {}
            for _ in range(self.fake.pyint(0, 3)):
                attributes.update(self.generate_attribute())

        if not archived or archived is ...:
            status = MetadataItemStatus.ACTIVE.value
        else:
            status = MetadataItemStatus.ARCHIVED.value

        return MetadataItemCreateSchema(
            id=id_,
            parent=parent,
            parent_path=parent_path,
            type=type_,
            zone=zone,
            name=name,
            size=size,
            owner=owner,
            container_code=container_code,
            container_type=container_type,
            created_time=created_time,
            last_updated_time=last_updated_time,
            tags=tags,
            template_id=template_id,
            template_name=template_name,
            attributes=attributes,
            status=status,
        )

    def generate_owner(self) -> str:
        return self.fake.unique.first_name().lower()

    def generate_zone(self) -> int:
        return self.fake.pyint(0, 1)

    def generate_size(self) -> int:
        return self.fake.pyint()

    def generate_container_code(self) -> str:
        return self.fake.unique.word().lower()

    def generate_attribute(self, name: str = ..., value: str = ...) -> dict:
        if name is ...:
            name = self.fake.word().lower()

        if value is ...:
            value = self.fake.word().lower()

        return {name: value}

    async def create(
        self,
        id_: UUID = ...,
        parent: UUID | None = ...,
        parent_path: str | None = ...,
        type_: MetadataItemType = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_id: UUID | None = ...,
        template_name: str | None = ...,
        attributes: dict[str, Any] | None = ...,
        archived: bool = ...,
        **kwds: Any,
    ) -> MetadataItem:
        entry = self.generate(
            id_,
            parent,
            parent_path,
            type_,
            zone,
            name,
            size,
            owner,
            container_code,
            container_type,
            created_time,
            last_updated_time,
            tags,
            template_id,
            template_name,
            attributes,
            archived,
        )

        params = {'refresh': 'true'}

        return await self.crud.create(entry, params=params, **kwds)

    async def create_name_folders(
        self,
        names: list[str],
        *,
        zone: int = ...,
        container_code: str = ...,
    ) -> ModelList[MetadataItem]:
        return ModelList(
            [
                await self.create(
                    parent=None,
                    type_=MetadataItemType.NAME_FOLDER,
                    zone=zone,
                    name=name,
                    owner=name,
                    container_code=container_code,
                )
                for name in names
            ]
        )

    async def create_file_for_parents(
        self,
        parents: list[MetadataItem],
        *,
        zone: int = ...,
        name: str = ...,
        container_code: str = ...,
    ) -> ModelList[MetadataItem]:
        return ModelList(
            [
                await self.create(
                    parent=parent.id,
                    parent_path=parent.name,
                    type_=MetadataItemType.FILE,
                    zone=zone,
                    name=name,
                    container_code=container_code,
                )
                for parent in parents
            ]
        )

    async def bulk_create(
        self,
        number: int,
        id_: UUID = ...,
        parent: UUID | None = ...,
        parent_path: str | None = ...,
        type_: MetadataItemType = ...,
        zone: int = ...,
        name: str = ...,
        size: int = ...,
        owner: str = ...,
        container_code: str = ...,
        container_type: ContainerType = ...,
        created_time: datetime = ...,
        last_updated_time: datetime = ...,
        tags: list[str] = ...,
        template_id: UUID | None = ...,
        template_name: str | None = ...,
        attributes: dict[str, Any] | None = ...,
        archived: bool = ...,
        **kwds: Any,
    ) -> ModelList[MetadataItem]:
        return ModelList(
            [
                await self.create(
                    id_,
                    parent,
                    parent_path,
                    type_,
                    zone,
                    name,
                    size,
                    owner,
                    container_code,
                    container_type,
                    created_time,
                    last_updated_time,
                    tags,
                    template_id,
                    template_name,
                    attributes,
                    archived,
                    **kwds,
                )
                for _ in range(number)
            ]
        )


@pytest.fixture
def metadata_item_crud(es_client) -> MetadataItemCRUD:
    yield MetadataItemCRUD(es_client)


@pytest.fixture
async def metadata_item_factory(metadata_item_crud, fake) -> MetadataItemFactory:
    metadata_item_factory = MetadataItemFactory(metadata_item_crud, fake)

    await metadata_item_factory.create_index()
    yield metadata_item_factory
    await metadata_item_factory.delete_index()
