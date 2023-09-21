# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from search.components.filtering import Filtering
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class ItemActivityProjectFileActivityFiltering(Filtering):
    """Item activities filtering for project file activity."""

    project_code: str
    activity_type: ItemActivityType
    from_date: datetime
    to_date: datetime
    user: str | None = None

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', self.project_code)
        search_query.match_term('activity_type', self.activity_type.value)
        search_query.match_range('activity_time', gte=int(self.from_date.timestamp()), lt=int(self.to_date.timestamp()))
        if self.user is not None:
            search_query.match_term('user', self.user)


class ItemActivityProjectFiltering(Filtering):
    """Item activity filtering control parameters."""

    activity_type: str | None = None
    activity_time_start: datetime | None = None
    activity_time_end: datetime | None = None
    container_code: str | None = None
    user: str | None = None
    zone: int | None = None

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        if self.activity_type:
            search_query.match_term('activity_type', self.activity_type)

        if self.activity_time_start:
            search_query.match_range('activity_time', gte=int(self.activity_time_start.timestamp()))

        if self.activity_time_end:
            search_query.match_range('activity_time', lte=int(self.activity_time_end.timestamp()))

        if self.container_code:
            search_query.match_term('container_code', self.container_code)

        search_query.match_term('container_type', ContainerType.PROJECT.value)

        if self.user:
            search_query.match_term('user', self.user)

        if self.zone:
            search_query.match_term('zone', self.zone)
