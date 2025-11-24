# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from search.components.filtering import Filtering
from search.components.metadata_item.models import MetadataItemStatus
from search.components.metadata_item.models import MetadataItemType
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class MetadataItemFiltering(Filtering):
    """Metadata items filtering control parameters."""

    name: str | None = None
    owner: str | None = None
    parent_path: str | None = None
    zone: int | None = None
    container_code: str | None = None
    container_type: ContainerType | None = None
    created_time_start: datetime | None = None
    created_time_end: datetime | None = None
    size_gte: int | None = None
    size_lte: int | None = None
    template_id: UUID | None = None
    attributes: dict[str, Any] | None = None
    is_archived: bool | None = None
    tags_all: str | None = None
    type: str | None = None

    def apply(self, search_query: SearchQuery) -> None:  # noqa: C901
        """Add filtering into search query."""

        if self.name:
            search_query.match_text('name.keyword', self.name)

        if self.owner:
            search_query.match_text('owner.keyword', self.owner)

        if self.parent_path:
            search_query.match_text('parent_path.keyword', self.parent_path)

        if self.zone is not None:
            search_query.match_term('zone', self.zone)

        if self.container_code:
            search_query.match_term('container_code', self.container_code)

        if self.container_type:
            search_query.match_term('container_type', self.container_type.value)

        if self.created_time_start:
            search_query.match_range('created_time', gte=int(self.created_time_start.timestamp()))

        if self.created_time_end:
            search_query.match_range('created_time', lte=int(self.created_time_end.timestamp()))

        if self.size_gte:
            search_query.match_range('size', gte=self.size_gte)

        if self.size_lte:
            search_query.match_range('size', lte=self.size_lte)

        if self.template_id:
            search_query.match_term('template_id', str(self.template_id))

        if self.attributes:
            search_query.init_nested('attributes')
            for key in self.attributes:
                value = self.attributes[key]
                if type(value) == str:
                    search_query.match_nested_contains('attributes', key, value)
                elif type(value) == list:
                    search_query.match_nested_exact('attributes', key, value)

        if self.is_archived is not None:
            status = MetadataItemStatus.ARCHIVED.value if self.is_archived else MetadataItemStatus.ACTIVE.value
            search_query.match_term('status.keyword', status)

        if self.tags_all:
            search_query.match_multiple_terms('tags', self.tags_all.split(','))

        if self.type:
            search_query.match_multiple_terms('type', self.type.split(','))


class MetadataItemProjectSizeUsageFiltering(Filtering):
    """Metadata items filtering for project size usage."""

    project_code: str
    parent_path: str | None = None
    from_date: datetime
    to_date: datetime

    def apply(self, search_query: SearchQuery) -> None:
        """Add filtering into search query."""

        search_query.match_term('type', MetadataItemType.FILE.value)
        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', self.project_code)
        search_query.match_range('created_time', gte=int(self.from_date.timestamp()), lt=int(self.to_date.timestamp()))
        search_query.match_term('status.keyword', MetadataItemStatus.ACTIVE.value)
        if self.parent_path is not None:
            search_query.match_text('parent_path.keyword', self.parent_path)
