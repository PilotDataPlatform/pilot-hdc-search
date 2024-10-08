# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from search.components.crud import CRUD
from search.components.metadata_item.crud.size_usage import SizeUsageHandler
from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.metadata_item.index import METADATA_ITEM_INDEX_MAPPINGS
from search.components.metadata_item.models import MetadataItem
from search.components.metadata_item.models import MetadataItemSizeStatistics
from search.components.metadata_item.models import MetadataItemSizeUsage
from search.components.metadata_item.models import MetadataItemStatus
from search.components.metadata_item.models import MetadataItemType
from search.components.metadata_item.models import SizeGroupBy
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class MetadataItemCRUD(CRUD):
    """CRUD for managing documents in metadata-items index."""

    index = 'metadata-items'
    index_mappings = METADATA_ITEM_INDEX_MAPPINGS
    model = MetadataItem

    async def get_project_size_usage(
        self, filtering: MetadataItemProjectSizeUsageFiltering, time_zone: str, group_by: SizeGroupBy
    ) -> MetadataItemSizeUsage:
        """Get aggregated project storage usage filtered by dates and grouped into separate buckets."""

        search_query = SearchQuery()
        filtering.apply(search_query)
        query = search_query.build()

        size_usage_handler = SizeUsageHandler(
            from_date=filtering.from_date, to_date=filtering.to_date, time_zone=time_zone, group_by=group_by
        )
        aggregations = size_usage_handler.get_aggregations()

        result = await self._search(query=query, size=0, aggregations=aggregations)

        return size_usage_handler.process_search_result(result)

    async def get_project_statistics(
        self, project_code: str, parent_path: str | None = None, zone: int | None = None
    ) -> MetadataItemSizeStatistics:
        """Get aggregated project files statistics."""
        search_query = SearchQuery()
        search_query.match_term('type', MetadataItemType.FILE.value)
        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', project_code)
        search_query.match_term('status.keyword', MetadataItemStatus.ACTIVE.value)
        if parent_path is not None:
            search_query.match_text('parent_path.keyword', parent_path)
        if zone is not None:
            search_query.match_term('zone', zone)

        query = search_query.build()

        aggregations = {'size': {'sum': {'field': 'size'}}}

        result = await self._search(query=query, size=0, aggregations=aggregations, track_total_hits=True)

        count = result['hits']['total']['value']
        size = int(result['aggregations']['size']['value'])

        return MetadataItemSizeStatistics(count=count, size=size)
