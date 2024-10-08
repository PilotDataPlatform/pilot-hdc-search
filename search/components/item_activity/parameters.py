# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from fastapi import Query

from search.components.item_activity.filtering import ItemActivityProjectFiltering
from search.components.parameters import FilterParameters
from search.components.parameters import SortByFields


class ItemActivitySortByFields(SortByFields):
    """Fields by which dataset activity logs can be sorted."""

    ACTIVITY_TIME = 'activity_time'


class ItemActivityFilterParameters(FilterParameters):
    """Query parameters for item activity filtering."""

    activity_type: str | None = Query(default=None)
    activity_time_start: datetime | None = Query(default=None)
    activity_time_end: datetime | None = Query(default=None)
    container_code: str | None = Query(default=None)
    user: str | None = Query(default=None)
    zone: int | None = Query(default=None)

    def to_filtering(self) -> ItemActivityProjectFiltering:
        return ItemActivityProjectFiltering(
            activity_type=self.activity_type,
            activity_time_start=self.activity_time_start,
            activity_time_end=self.activity_time_end,
            container_code=self.container_code,
            user=self.user,
            zone=self.zone,
        )
