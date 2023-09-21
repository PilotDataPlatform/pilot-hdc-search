# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
from datetime import datetime
from uuid import UUID

from fastapi import Query
from pydantic import PositiveInt
from pydantic import validator

from search.components.metadata_item.filtering import MetadataItemFiltering
from search.components.models import ContainerType
from search.components.parameters import FilterParameters
from search.components.parameters import SortByFields


class MetadataItemSortByFields(SortByFields):
    """Fields by which metadata items can be sorted."""

    SIZE = 'size'
    CREATED_TIME = 'created_time'
    LAST_UPDATED_TIME = 'last_updated_time'


class MetadataItemFilterParameters(FilterParameters):
    """Query parameters for metadata items filtering."""

    name: str | None = Query(default=None)
    owner: str | None = Query(default=None)
    parent_path: str | None = Query(default=None)
    zone: int | None = Query(default=None)
    container_code: str | None = Query(default=None)
    container_type: ContainerType | None = Query(default=None)
    created_time_start: datetime | None = Query(default=None)
    created_time_end: datetime | None = Query(default=None)
    size_gte: PositiveInt | None = Query(default=None)
    size_lte: PositiveInt | None = Query(default=None)
    template_id: UUID | None = Query(default=None)
    attributes: str | None = Query(default=None)
    is_archived: bool | None = Query(default=None)
    tags_all: str | None = Query(default=None)
    type: str | None = Query(default=None)

    @validator('attributes')
    def attributes_validation(cls, v):
        if v:
            try:
                json.loads(v)
            except ValueError:
                raise ValueError('Must be valid JSON')
        return v

    def to_filtering(self) -> MetadataItemFiltering:
        return MetadataItemFiltering(
            name=self.name,
            owner=self.owner,
            parent_path=self.parent_path,
            zone=self.zone,
            container_code=self.container_code,
            container_type=self.container_type,
            created_time_start=self.created_time_start,
            created_time_end=self.created_time_end,
            size_gte=self.size_gte,
            size_lte=self.size_lte,
            template_id=self.template_id,
            attributes=json.loads(self.attributes) if self.attributes else None,
            is_archived=self.is_archived,
            tags_all=self.tags_all,
            type=self.type,
        )
