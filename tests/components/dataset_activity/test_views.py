# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest

from search.components.dataset_activity.schemas import DatasetActivityIndexedSchema
from search.components.dataset_activity.schemas import ItemActivityIndexedSchema


class TestDatasetAndItemActivityLogsViews:
    async def test_list_dataset_activity_returns_list_of_existing_dataset_activities(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await dataset_activity_factory.bulk_create(3)

        response = await client.get('/v1/dataset-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 3

    async def test_list_dataset_activity_returns_list_of_existing_item_activities(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await item_activity_factory.bulk_create(3)

        response = await client.get('/v1/dataset-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 3

    async def test_list_dataset_activity_returns_list_of_existing_item_and_dataset_activities_with_correct_schemas(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await item_activity_factory.bulk_create(3)
        await dataset_activity_factory.bulk_create(3)

        response = await client.get('/v1/dataset-activity-logs/')

        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()

        assert received_total == 6

        item_activity_logs = body('.result[] | select(.index=="file")').all()
        dataset_activity_logs = body('.result[] | select(.index=="dataset")').all()

        assert len(item_activity_logs) == 3
        assert len(dataset_activity_logs) == 3

        for f in item_activity_logs:
            assert f.keys() == ItemActivityIndexedSchema.schema()['properties'].keys()

        for d in dataset_activity_logs:
            assert d.keys() == DatasetActivityIndexedSchema.schema()['properties'].keys()

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
    async def test_list_dataset_activity_returns_properly_paginated_response(
        self, items_number, page, page_size, expected_count, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await dataset_activity_factory.bulk_create(items_number)

        response = await client.get('/v1/dataset-activity-logs/', params={'page': page, 'page_size': page_size})

        assert response.status_code == 200

        body = jq(response)
        received_dataset_activity_logs_cc = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert len(received_dataset_activity_logs_cc) == expected_count
        assert received_total == items_number

    @pytest.mark.parametrize('parameter', ['version', 'target_name', 'user'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_full_text_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_dataset_activity = await dataset_activity_factory.bulk_create(3)
        await item_activity_factory.bulk_create(3)
        dataset_activity = created_dataset_activity.pop()

        response = await client.get(
            '/v1/dataset-activity-logs/', params={parameter: getattr(dataset_activity, parameter)}
        )

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()
        received_dataset_activity = body('.result[]').first()

        assert received_ccs == [dataset_activity.container_code]
        assert received_total == 1
        assert received_dataset_activity.keys() == DatasetActivityIndexedSchema.schema()['properties'].keys()

    @pytest.mark.parametrize('parameter', ['version', 'target_name', 'user'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_partial_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_dataset_activities = await dataset_activity_factory.bulk_create(3)
        await item_activity_factory.bulk_create(3)
        dataset_activity = created_dataset_activities.pop()
        value = getattr(dataset_activity, parameter)
        lookup = value.replace(value[5:], '%')

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: lookup})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()
        received_dataset_activity = body('.result[]').first()

        assert received_ccs == [dataset_activity.container_code]
        assert received_total == 1
        assert received_dataset_activity.keys() == DatasetActivityIndexedSchema.schema()['properties'].keys()

    @pytest.mark.parametrize('parameter', ['item_name'])
    async def test_list_dataset_activities_returns_item_activity_filtered_by_parameter_partial_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_item_activity = await item_activity_factory.bulk_create(3)
        await dataset_activity_factory.bulk_create(3)
        item_activity = created_item_activity.pop()

        value = getattr(item_activity, parameter)
        lookup = value.replace(value[5:], '%')

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: lookup})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()
        received_item_activity = body('.result[]').first()

        assert received_ccs == [item_activity.container_code]
        assert received_total == 1
        assert received_item_activity.keys() == ItemActivityIndexedSchema.schema()['properties'].keys()

    @pytest.mark.parametrize('parameter', ['item_name', 'item_parent_path'])
    async def test_list_dataset_activities_returns_item_activity_filtered_by_parameter_full_text_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_item_activity = await item_activity_factory.bulk_create(3)
        await dataset_activity_factory.bulk_create(3)
        item_activity = created_item_activity.pop()

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: getattr(item_activity, parameter)})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()
        received_item_activity = body('.result[]').first()

        assert received_ccs == [item_activity.container_code]
        assert received_total == 1
        assert received_item_activity.keys() == ItemActivityIndexedSchema.schema()['properties'].keys()

    @pytest.mark.parametrize('parameter', ['activity_type', 'container_code'])
    async def test_list_dataset_activities_returns_dataset_activity_filtered_by_parameter_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_dataset_activities = await dataset_activity_factory.bulk_create(3)
        value = getattr(created_dataset_activities[0], parameter)
        expected_ccs = {
            dataset.container_code for dataset in created_dataset_activities if getattr(dataset, parameter) == value
        }

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: value})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert set(received_ccs) == expected_ccs
        assert received_total == len(expected_ccs)

    @pytest.mark.parametrize(
        'parameter',
        ['activity_type', 'container_code', 'item_type', 'item_id', 'zone', 'container_type', 'imported_from'],
    )
    async def test_list_dataset_activities_returns_item_activity_filtered_by_parameter_match(
        self, parameter, client, jq, dataset_activity_factory, item_activity_factory
    ):
        created_item_activities = await item_activity_factory.bulk_create(3)
        value = getattr(created_item_activities[0], parameter)
        expected_ccs = {item.container_code for item in created_item_activities if getattr(item, parameter) == value}

        response = await client.get('/v1/dataset-activity-logs/', params={parameter: str(value)})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert set(received_ccs) == expected_ccs
        assert received_total == len(expected_ccs)

    async def test_list_dataset_activities_returns_item_activity_and_dataset_activity_filtered_by_container_code(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await item_activity_factory.bulk_create(3)
        await dataset_activity_factory.bulk_create(3)
        container_code = 'test_container'
        await item_activity_factory.create(container_code=container_code)
        await dataset_activity_factory.create(container_code=container_code)

        response = await client.get('/v1/dataset-activity-logs/', params={'container_code': container_code})

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()
        received_index = body('.result[].index').all()

        assert received_ccs == [container_code] * 2
        assert received_total == 2
        assert set(received_index) == {'dataset', 'file'}

    async def test_list_dataset_activities_returns_dataset_and_item_activities_filtered_by_activity_time_parameters(
        self, client, jq, fake, dataset_activity_factory, item_activity_factory
    ):
        today = datetime.now(tz=timezone.utc)
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [
            await dataset_activity_factory.create(activity_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]
        [
            await item_activity_factory.create(activity_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]
        dataset_activity = await dataset_activity_factory.create(
            activity_time=fake.date_time_between_dates(week_ago, today)
        )
        item_activity = await item_activity_factory.create(activity_time=fake.date_time_between_dates(week_ago, today))

        params = {
            'activity_time_start': int(datetime.timestamp(week_ago)),
            'activity_time_end': int(datetime.timestamp(today)),
        }
        response = await client.get('/v1/dataset-activity-logs/', params=params)

        body = jq(response)
        received_ccs = body('.result[].container_code').all()
        received_total = body('.total').first()

        assert set(received_ccs) == {dataset_activity.container_code, item_activity.container_code}
        assert received_total == 2

    async def test_list_dataset_activities_with_fields_that_may_contain_none_values(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await dataset_activity_factory.create(target_name=None)
        await dataset_activity_factory.create(version=None)
        changes = {'property': 'test', 'old_value': None, 'new_value': None}
        await dataset_activity_factory.create(changes=[changes])

        response = await client.get('/v1/dataset-activity-logs/')
        assert response.status_code == 200

        body = jq(response)
        received_total = body('.total').first()
        assert received_total == 3

        targets = body('.result[].target_name').all()
        versions = body('.result[].version').all()
        changes_res = body('.result[].changes').all()

        assert None in targets
        assert None in versions
        assert [changes] in changes_res

    async def test_list_item_activities_with_fields_that_may_contain_none_values(
        self, client, jq, dataset_activity_factory, item_activity_factory
    ):
        await item_activity_factory.create(item_id=None)
        await item_activity_factory.create(imported_from=None)
        changes = {'item_property': 'test', 'old_value': None, 'new_value': None}
        await item_activity_factory.create(changes=[changes])

        response = await client.get('/v1/dataset-activity-logs/')
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
