# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from search.components.encoders import datetime_as_timestamp_encoder
from search.components.item_activity.models import ItemActivityChange
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.schemas import BaseSchema
from search.components.schemas import ListResponseSchema


class ItemActivitySchema(BaseSchema):
    """General item activity schema."""

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


class ItemActivityCreateSchema(ItemActivitySchema, json_encoders=datetime_as_timestamp_encoder):
    """Item activity schema used for creation."""


class ItemActivityListResponseSchema(ListResponseSchema):
    """Default schema for item activities in response."""

    result: list[ItemActivitySchema]
