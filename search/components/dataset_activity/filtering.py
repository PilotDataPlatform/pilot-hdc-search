# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from search.components.filtering import Filtering
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class DatasetAndItemActivityFiltering(Filtering):
    """Dataset and item activity filtering control parameters."""

    activity_type: str | None = None
    activity_time_start: datetime | None = None
    activity_time_end: datetime | None = None
    container_code: str | None = None
    version: str | None = None
    target_name: str | None = None
    user: str | None = None
    container_type: ContainerType | None = None
    item_id: UUID | None = None
    item_type: str | None = None
    item_name: str | None = None
    item_parent_path: str | None = None
    zone: int | None = None
    imported_from: str | None = None

    def apply(self, search_query: SearchQuery) -> None:  # noqa: C901
        """Add filtering into search query."""

        if self.activity_type:
            search_query.match_term('activity_type', self.activity_type)

        if self.activity_time_start:
            search_query.match_range('activity_time', gte=int(self.activity_time_start.timestamp()))

        if self.activity_time_end:
            search_query.match_range('activity_time', lte=int(self.activity_time_end.timestamp()))

        if self.container_code:
            search_query.match_term('container_code', self.container_code)

        if self.version:
            search_query.match_text('version', self.version)

        if self.target_name:
            search_query.match_text('target_name', self.target_name)

        if self.user:
            search_query.match_text('user', self.user)

        if self.container_type:
            search_query.match_term('container_type', self.container_type)

        if self.item_id:
            search_query.match_term('item_id', str(self.item_id))

        if self.item_name:
            search_query.match_text('item_name', self.item_name)

        if self.item_type:
            search_query.match_term('item_type', self.item_type)

        if self.item_parent_path:
            search_query.match_text('item_parent_path', self.item_parent_path)

        if self.zone:
            search_query.match_term('zone', self.zone)

        if self.imported_from:
            search_query.match_term('imported_from', self.imported_from)
