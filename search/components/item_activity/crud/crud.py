# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import time
from datetime import timezone

from search.components.crud import CRUD
from search.components.item_activity.crud.file_activity import FileActivityHandler
from search.components.item_activity.filtering import ItemActivityProjectFileActivityFiltering
from search.components.item_activity.index import ITEM_ACTIVITY_INDEX_MAPPINGS
from search.components.item_activity.models import ActivityGroupBy
from search.components.item_activity.models import ItemActivity
from search.components.item_activity.models import ItemActivityTransferStatistics
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType
from search.components.search_query import SearchQuery


class ItemActivityCRUD(CRUD):
    """CRUD for managing documents in items-activity-logs index."""

    index = 'items-activity-logs'
    index_mappings = ITEM_ACTIVITY_INDEX_MAPPINGS
    model = ItemActivity

    async def get_project_transfer_statistics(
        self, project_code: str, date: datetime, time_zone: str, parent_path: str | None = None, zone: int | None = None
    ) -> ItemActivityTransferStatistics:
        """Get aggregated project transfer statistics."""
        parsed_tz = datetime.strptime(time_zone, '%z')
        day_considering_timezone = date.astimezone(tz=parsed_tz.tzinfo).date()
        start_of_day = datetime.combine(day_considering_timezone, time(0, 0, 0, tzinfo=timezone.utc))
        end_of_day = datetime.combine(day_considering_timezone, time(23, 59, 59, tzinfo=timezone.utc))

        search_query = SearchQuery()
        search_query.match_term('container_type', ContainerType.PROJECT.value)
        search_query.match_term('container_code', project_code)
        search_query.match_range('activity_time', gte=int(start_of_day.timestamp()), lte=int(end_of_day.timestamp()))
        search_query.match_multiple_terms(
            'activity_type', [ItemActivityType.UPLOAD.value, ItemActivityType.DOWNLOAD.value]
        )
        if parent_path is not None:
            search_query.match_text('item_parent_path.keyword', parent_path)
        if zone is not None:
            search_query.match_term('zone', zone)

        query = search_query.build()

        aggregations = {'activity_types': {'terms': {'field': 'activity_type'}}}

        result = await self._search(query=query, size=0, aggregations=aggregations)

        mapping = {
            ItemActivityType.UPLOAD: 0,
            ItemActivityType.DOWNLOAD: 0,
        }

        for bucket in result['aggregations']['activity_types']['buckets']:
            try:
                mapping[bucket['key']] += bucket['doc_count']
            except KeyError:
                pass

        return ItemActivityTransferStatistics(
            uploaded=mapping[ItemActivityType.UPLOAD],
            downloaded=mapping[ItemActivityType.DOWNLOAD],
        )

    async def get_project_file_activity(
        self, filtering: ItemActivityProjectFileActivityFiltering, time_zone: str, group_by: ActivityGroupBy
    ) -> dict[str, int]:
        """Get aggregated project file activity filtered by dates and grouped into separate buckets."""
        search_query = SearchQuery()
        filtering.apply(search_query)
        query = search_query.build()

        file_activity_handler = FileActivityHandler(
            from_date=filtering.from_date, to_date=filtering.to_date, time_zone=time_zone, group_by=group_by
        )
        aggregations = file_activity_handler.get_aggregations()

        result = await self._search(query=query, size=0, aggregations=aggregations)

        return file_activity_handler.process_search_result(result)
