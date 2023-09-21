# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from search.components.metadata_item.crud.size_usage import SizeUsageHandler
from search.components.metadata_item.models import SizeGroupBy


class TestSizeUsageHandler:
    def test_get_grouping_keys_returns_4_months_when_february_is_inbetween_and_from_date_is_last_day_of_the_month(self):
        size_usage_handler = SizeUsageHandler(
            from_date=datetime(2022, 1, 31),
            to_date=datetime(2022, 5, 31),
            time_zone='+00:00',
            group_by=SizeGroupBy.MONTH,
        )
        expected_keys = ['2022-01', '2022-02', '2022-03', '2022-04']
        received_keys = size_usage_handler.get_grouping_keys()

        assert received_keys == expected_keys
