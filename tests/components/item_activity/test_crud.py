# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import timedelta

from search.components.item_activity.filtering import ItemActivityProjectFileActivityFiltering
from search.components.item_activity.models import ActivityGroupBy
from search.components.item_activity.models import ItemActivityTransferStatistics
from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType


class TestItemActivityCRUD:
    async def test_get_project_transfer_statistics_returns_valid_stats_considering_activity_time(
        self, fake, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime_utc().replace(hour=12)
        for activity_type in [ItemActivityType.DOWNLOAD, ItemActivityType.UPLOAD]:
            await item_activity_factory.bulk_create(
                2, container_code=project_code, activity_time=activity_time, activity_type=activity_type
            )

        received_transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
            project_code, activity_time, '+00:00'
        )

        assert received_transfer_statistics == ItemActivityTransferStatistics(uploaded=2, downloaded=2)

    async def test_get_project_transfer_statistics_returns_valid_stats_considering_activity_time_and_time_zone(
        self, fake, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime_utc().replace(hour=22)
        for hours in range(0, 9, 3):
            await item_activity_factory.create(
                container_code=project_code,
                activity_time=activity_time + timedelta(hours=hours),
                activity_type=ItemActivityType.DOWNLOAD,
            )

        received_transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
            project_code, activity_time, '+05:00'
        )

        assert received_transfer_statistics == ItemActivityTransferStatistics(uploaded=0, downloaded=2)

    async def test_get_project_file_activity_returns_project_activity_grouped_by_day(
        self, fake, item_activity_crud, item_activity_factory
    ):
        to_date = fake.past_datetime_utc()
        from_date = to_date - timedelta(days=3)
        project_code = fake.word().lower()
        expected_file_activity = {}

        for day in range(3):
            activity_time = from_date + timedelta(days=day)
            created_item_activity = await item_activity_factory.create(
                container_type=ContainerType.PROJECT, container_code=project_code, activity_time=activity_time
            )
            key = activity_time.strftime('%Y-%m-%d')
            value = 1 if created_item_activity.activity_type == ItemActivityType.DOWNLOAD else 0
            expected_file_activity[key] = value

        filtering = ItemActivityProjectFileActivityFiltering(
            project_code=project_code, activity_type=ItemActivityType.DOWNLOAD, from_date=from_date, to_date=to_date
        )
        received_file_activity = await item_activity_crud.get_project_file_activity(
            filtering, '+00:00', ActivityGroupBy.DAY
        )

        assert received_file_activity == expected_file_activity
