# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from typing import Any

from dateutil.rrule import MONTHLY
from dateutil.rrule import rrule
from pydantic import BaseModel

from search.components.metadata_item.models import MetadataItemSizeUsage
from search.components.metadata_item.models import MetadataItemSizeUsageDataset
from search.components.metadata_item.models import SizeGroupBy


class SizeUsageHandler(BaseModel):
    """Process aggregated response to provide size usage statistic.

    Only grouping by month is supported at the moment, so it's hardcoded.
    """

    from_date: datetime
    to_date: datetime
    time_zone: str
    group_by: SizeGroupBy

    @property
    def grouping_interval(self) -> str:
        return SizeGroupBy.MONTH.value

    @property
    def elasticsearch_grouping_format(self) -> str:
        return 'yyyy-MM'

    @property
    def manual_grouping_format(self) -> str:
        return '%Y-%m'

    def get_grouping_keys(self) -> list[str]:
        """Return list of keys that will be used for each bucket."""

        dates_range = rrule(MONTHLY, dtstart=self.from_date, until=self.to_date - timedelta(seconds=1), bymonthday=-1)
        keys = {date.strftime(self.manual_grouping_format) for date in dates_range}
        return sorted(keys)

    def get_aggregations(self) -> dict[str, Any]:
        """Return aggregations to retrieve data."""

        return {
            'group_by_zone': {
                'terms': {'field': 'zone'},
                'aggs': {
                    'group_by_created_time': {
                        'date_histogram': {
                            'field': 'created_time',
                            'calendar_interval': self.grouping_interval,
                            'min_doc_count': 0,
                            'time_zone': self.time_zone,
                            'format': self.elasticsearch_grouping_format,
                            'keyed': True,
                        },
                        'aggs': {
                            'total_size': {'sum': {'field': 'size'}},
                        },
                    },
                },
            },
        }

    def process_search_result(self, result: dict[str, Any]) -> MetadataItemSizeUsage:
        """Process search result and categorize into datasets per zone."""

        buckets_by_zone = result['aggregations']['group_by_zone']['buckets']
        available_zones = {zone['key'] for zone in buckets_by_zone}

        grouping_keys = self.get_grouping_keys()

        if not available_zones:
            return MetadataItemSizeUsage(labels=grouping_keys, datasets=[])

        mapping = defaultdict(dict)
        for key in grouping_keys:
            for zone in available_zones:
                mapping[key][zone] = 0

        for zone in buckets_by_zone:
            zone_key = zone['key']
            buckets_by_created_time = zone['group_by_created_time']['buckets']
            for date_key, date in buckets_by_created_time.items():
                mapping[date_key][zone_key] = int(date['total_size']['value'])

        datasets = []
        for zone in available_zones:
            values = [mapping[key][zone] for key in grouping_keys]
            datasets.append(MetadataItemSizeUsageDataset(label=zone, values=values))

        return MetadataItemSizeUsage(labels=grouping_keys, datasets=datasets)
