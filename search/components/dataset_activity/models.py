# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from pydantic import BaseModel

from search.components.item_activity.models import ItemActivity
from search.components.item_activity.models import ItemActivityChange
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.types import StrEnum


class DatasetAndItemActivityIndex(StrEnum):
    """Store information which index the model belongs to.

    Internally we use ITEM but outside we expose this as "file".
    """

    ITEM = 'file'
    DATASET = 'dataset'


class DatasetActivityType(StrEnum):
    """Store all available dataset activity types."""

    DOWNLOAD = 'download'
    UPDATE = 'update'
    CREATE = 'create'
    RELEASE = 'release'
    SCHEMA_DELETE = 'schema_delete'
    SCHEMA_UPDATE = 'schema_update'
    SCHEMA_CREATE = 'schema_create'
    TEMPLATE_DELETE = 'template_delete'
    TEMPLATE_UPDATE = 'template_update'
    TEMPLATE_CREATE = 'template_create'


class DatasetActivityChange(BaseModel):
    """Dataset activity change model."""

    property: str
    old_value: str | None
    new_value: str | None


class DatasetActivity(BaseModel):
    """Dataset activity elasticsearch document model."""

    activity_type: DatasetActivityType
    activity_time: datetime
    container_code: str
    version: str | None
    target_name: str | None
    user: str
    changes: list[DatasetActivityChange]


class DatasetAndItemActivity(DatasetActivity, ItemActivity):
    """Combined dataset and item activity elasticsearch document model."""

    index: DatasetAndItemActivityIndex

    # Combined from two models
    activity_type: DatasetActivityType | ItemActivityType
    changes: list[DatasetActivityChange | ItemActivityChange]

    # Item activity model fields should be nullable
    container_type: ContainerType | None
    item_type: str | None
    item_name: str | None
    item_parent_path: str | None
    zone: int | None
    imported_from: str | None
