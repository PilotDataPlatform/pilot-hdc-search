# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from fastapi import Query

from search.components.dataset_activity.filtering import DatasetAndItemActivityFiltering
from search.components.models import ContainerType
from search.components.parameters import FilterParameters
from search.components.parameters import SortByFields


class DatasetActivitySortByFields(SortByFields):
    """Fields by which dataset activity logs can be sorted."""

    ACTIVITY_TIME = 'activity_time'


class DatasetAndItemActivityFilterParameters(FilterParameters):
    """Query parameters for dataset and item activity filtering."""

    activity_type: str | None = Query(default=None)
    activity_time_start: datetime | None = Query(default=None)
    activity_time_end: datetime | None = Query(default=None)
    container_code: str | None = Query(default=None)
    version: str | None = Query(default=None)
    target_name: str | None = Query(default=None)
    user: str | None = Query(default=None)
    container_type: ContainerType | None = Query(default=None)
    item_id: UUID | None = Query(default=None)
    item_type: str | None = Query(default=None)
    item_name: str | None = Query(default=None)
    item_parent_path: str | None = Query(default=None)
    zone: int | None = Query(default=None)
    imported_from: str | None = Query(default=None)

    def to_filtering(self) -> DatasetAndItemActivityFiltering:
        return DatasetAndItemActivityFiltering(
            activity_type=self.activity_type,
            activity_time_start=self.activity_time_start,
            activity_time_end=self.activity_time_end,
            container_code=self.container_code,
            version=self.version,
            target_name=self.target_name,
            user=self.user,
            container_type=self.container_type,
            item_id=self.item_id,
            item_type=self.item_type,
            item_name=self.item_name,
            item_parent_path=self.item_parent_path,
            zone=self.zone,
            imported_from=self.imported_from,
        )
