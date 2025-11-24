# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Annotated
from typing import Any
from typing import Literal

from pydantic import Field

from search.components.dataset_activity.models import DatasetActivityType
from search.components.dataset_activity.models import DatasetAndItemActivityIndex
from search.components.encoders import datetime_as_timestamp_encoder
from search.components.item_activity.schemas import ItemActivitySchema
from search.components.schemas import BaseSchema
from search.components.schemas import ListResponseSchema


class DatasetActivitySchema(BaseSchema):
    """Dataset activity schema."""

    activity_type: DatasetActivityType
    activity_time: datetime
    container_code: str
    version: str | None
    target_name: str | None
    user: str
    changes: list[dict[str, Any]]
    network_origin: str


class DatasetActivityCreateSchema(DatasetActivitySchema, json_encoders=datetime_as_timestamp_encoder):
    """Dataset activity schema used for creation."""


class DatasetActivityIndexedSchema(DatasetActivitySchema):
    """Dataset activity schema with source index."""

    index: Literal[DatasetAndItemActivityIndex.DATASET]


class ItemActivityIndexedSchema(ItemActivitySchema):
    """Item activity schema with source index."""

    index: Literal[DatasetAndItemActivityIndex.ITEM]


class DatasetAndItemActivityListResponseSchema(ListResponseSchema):
    """Default schema for multiple dataset and item activities in response."""

    result: list[Annotated[DatasetActivityIndexedSchema | ItemActivityIndexedSchema, Field(discriminator='index')]]
