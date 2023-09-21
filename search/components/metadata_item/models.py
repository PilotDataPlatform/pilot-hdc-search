# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from search.components.models import ContainerType
from search.components.types import StrEnum


class SizeGroupBy(StrEnum):
    """Store possible group by options for metadata items."""

    MONTH = 'month'


class MetadataItemType(StrEnum):
    """Store all metadata item types."""

    FILE = 'file'
    FOLDER = 'folder'
    NAME_FOLDER = 'name_folder'


class MetadataItemAttribute(BaseModel):
    """Metadata item attribute structure."""

    name: str
    value: str


class MetadataItemStatus(StrEnum):
    """Store status of metadata item."""

    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'


class MetadataItem(BaseModel):
    """Metadata item elasticsearch document model."""

    pk: str
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


class MetadataItemSizeUsageDataset(BaseModel):
    """Metadata item size usage dataset structure."""

    label: int
    values: list[int]


class MetadataItemSizeUsage(BaseModel):
    """Metadata item size usage model."""

    labels: list[str]
    datasets: list[MetadataItemSizeUsageDataset]


class MetadataItemSizeStatistics(BaseModel):
    """Metadata item size statistics model."""

    count: int
    size: int
