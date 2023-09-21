# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from search.components.encoders import datetime_as_timestamp_encoder
from search.components.metadata_item.models import MetadataItemStatus
from search.components.models import ContainerType
from search.components.schemas import BaseSchema
from search.components.schemas import ListResponseSchema


class MetadataItemSchema(BaseSchema):
    """General metadata item schema."""

    id: UUID
    parent: UUID | None
    parent_path: str | None
    type: str
    zone: int
    name: str
    size: int
    owner: str
    container_code: str
    container_type: ContainerType
    created_time: datetime
    last_updated_time: datetime
    tags: list[str]
    template_id: UUID | None
    template_name: str | None
    attributes: dict[str, Any] | None
    status: MetadataItemStatus


class MetadataItemCreateSchema(MetadataItemSchema, json_encoders=datetime_as_timestamp_encoder):
    """Metadata item schema used for creation."""


class MetadataItemResponseSchema(MetadataItemSchema):
    """Default schema for single metadata item in response."""

    pk: str


class MetadataItemListResponseSchema(ListResponseSchema):
    """Default schema for multiple metadata items in response."""

    result: list[MetadataItemResponseSchema]
