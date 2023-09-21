# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest

from search.components.item_activity.models import ItemActivityType
from search.components.models import ContainerType


class TestItemActivityLogsViews:
    async def test_get_project_item_activity_logs_returns_list_of_existing_item_activities(
        self, fake, client, jq, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime_utc().replace(hour=12)
        for activity_type in [ItemActivityType.DOWNLOAD, ItemActivityType.UPLOAD]:
            await item_activity_factory.bulk_create(
                2, container_code=project_code, activity_time=activity_time, activity_type=activity_type
            )

        response = await client.get('/v1/item-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 4

    async def test_get_project_item_activity_logs_returns_list_of_existing_item_activities_for_only_projects(
        self, fake, client, jq, item_activity_crud, item_activity_factory
    ):

        await item_activity_factory.bulk_create(1, container_type=ContainerType.DATASET)
        await item_activity_factory.bulk_create(1, container_type=ContainerType.PROJECT)

        response = await client.get('/v1/item-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()
        received_activity = body('.result').first()[0]

        assert received_total == 1
        assert received_activity['container_type'] == ContainerType.PROJECT.value

    @pytest.mark.parametrize(
        'items_number,page,page_size,expected_count',
        [
            (4, 1, 3, 3),
            (4, 2, 3, 1),
            (2, 1, 3, 2),
            (2, 2, 1, 1),
            (2, 3, 1, 0),
        ],
    )
    async def test_get_project_item_activity_logs_returns_properly_paginated_response(
        self, fake, client, items_number, page, page_size, expected_count, jq, item_activity_crud, item_activity_factory
    ):
        project_code = fake.word().lower()
        activity_time = fake.past_datetime_utc().replace(hour=12)
        for activity_type in [ItemActivityType.DOWNLOAD]:
            await item_activity_factory.bulk_create(
                items_number, container_code=project_code, activity_time=activity_time, activity_type=activity_type
            )

        response = await client.get('/v1/item-activity-logs/', params={'page': page, 'page_size': page_size})

        assert response.status_code == 200

        body = jq(response)
        received_item_activity_logs_cc = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert len(received_item_activity_logs_cc) == expected_count
        assert received_total == items_number

    async def test_get_project_item_activity_logs_returns_item_activity_filtered_by_container_code(
        self, fake, client, jq, item_activity_crud, item_activity_factory
    ):
        container_code = fake.word().lower()
        await item_activity_factory.bulk_create(3)
        await item_activity_factory.create(container_code=container_code)

        response = await client.get('/v1/item-activity-logs/', params={'container_code': container_code})

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 1

    @pytest.mark.parametrize(
        'parameter',
        ['activity_type', 'container_code', 'zone', 'user'],
    )
    async def test_get_project_item_activity_logs_returns_item_activity_filtered_by_parameter_match(
        self, fake, client, jq, parameter, item_activity_crud, item_activity_factory
    ):
        created_item_activities = await item_activity_factory.bulk_create(3)
        value = getattr(created_item_activities[0], parameter)
        expected_ccs = {item.container_code for item in created_item_activities if getattr(item, parameter) == value}

        response = await client.get('/v1/item-activity-logs/', params={parameter: str(value)})

        assert response.status_code == 200

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert set(received_ccs) == expected_ccs
        assert received_total == len(expected_ccs)

    async def test_get_project_item_activity_logs_returns_item_activity_filtered_by_activity_time(
        self, fake, client, jq, item_activity_crud, item_activity_factory
    ):
        today = datetime.now(tz=timezone.utc)
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [
            await item_activity_factory.create(activity_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]

        item_activity = await item_activity_factory.create(activity_time=fake.date_time_between_dates(week_ago, today))

        params = {
            'activity_time_start': int(datetime.timestamp(week_ago)),
            'activity_time_end': int(datetime.timestamp(today)),
        }

        response = await client.get('/v1/item-activity-logs/', params=params)

        assert response.status_code == 200

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert received_total == 1
        assert set(received_ccs) == {item_activity.container_code}

    async def test_get_project_item_activity_logs_returns_item_activity_with_fields_that_may_contain_none_values(
        self, fake, client, jq, item_activity_crud, item_activity_factory
    ):

        await item_activity_factory.create(item_id=None)
        await item_activity_factory.create(imported_from=None)
        changes = {'item_property': 'test', 'old_value': None, 'new_value': None}
        await item_activity_factory.create(changes=[changes])

        response = await client.get('/v1/item-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()
        assert received_total == 3

        item_id = body('.result[].item_id').all()
        imported_from = body('.result[].imported_from').all()
        changes_res = body('.result[].changes').all()

        assert None in item_id
        assert None in imported_from
        assert [changes] in changes_res
