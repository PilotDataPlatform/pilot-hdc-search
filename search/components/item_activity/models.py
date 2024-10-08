# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from search.components.models import ContainerType
from search.components.types import StrEnum


class ActivityGroupBy(StrEnum):
    """Store possible group by options for item activities."""

    DAY = 'day'


class ItemActivityType(StrEnum):
    """Store all available item activity types."""

    DOWNLOAD = 'download'
    UPLOAD = 'upload'
    DELETE = 'delete'
    COPY = 'copy'
    IMPORT = 'import'
    CREATE = 'create'
    APPROVE = 'approve'
    UPDATE = 'update'


class ItemActivityChange(BaseModel):
    """Items activity change model."""

    item_property: str
    old_value: str | None
    new_value: str | None


class ItemActivity(BaseModel):
    """Item activity elasticsearch document model."""

    pk: str
    activity_type: ItemActivityType
    activity_time: datetime
    container_code: str
    container_type: ContainerType
    item_id: UUID | None
    item_type: str
    item_name: str
    item_parent_path: str
    zone: int
    user: str
    imported_from: str | None
    changes: list[ItemActivityChange]


class ItemActivityTransferStatistics(BaseModel):
    """Item activity transfer statistics model."""

    uploaded: int
    downloaded: int
