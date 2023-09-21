# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from search.components.item_activity.models import ItemActivityType
from search.components.metadata_item.models import MetadataItemType


class TestProjectFilesViews:
    async def test_get_project_size_usage_returns_project_storage_usage_datasets_grouped_by_zone(
        self, client, jq, metadata_item_factory
    ):
        created_metadata_item = await metadata_item_factory.create(type_=MetadataItemType.FILE)
        from_date = (created_metadata_item.created_time - timedelta(days=1)).isoformat()
        to_date = (created_metadata_item.created_time + timedelta(days=1)).isoformat()

        response = await client.get(
            f'/v1/project-files/{created_metadata_item.container_code}/size',
            params={'from': from_date, 'to': to_date, 'time_zone': '+00:00'},
        )

        assert response.status_code == 200

        body = jq(response)
        received_zone = body('.data.datasets[].label').first()

        assert received_zone == created_metadata_item.zone

    async def test_get_project_statistics_returns_files_and_transfer_activity_statistics(
        self, fake, client, metadata_item_factory, item_activity_factory
    ):
        project_code = metadata_item_factory.generate_container_code()
        time = datetime.now(tz=timezone.utc)
        created_metadata_item = await metadata_item_factory.create(
            container_code=project_code, created_time=time, type_=MetadataItemType.FILE
        )
        await item_activity_factory.create(
            container_code=project_code, activity_time=time, activity_type=ItemActivityType.UPLOAD
        )

        expected_response = {
            'files': {
                'total_count': 1,
                'total_size': created_metadata_item.size,
            },
            'activity': {
                'today_uploaded': 1,
                'today_downloaded': 0,
            },
        }

        response = await client.get(f'/v1/project-files/{project_code}/statistics', params={'time_zone': '+00:00'})

        assert response.status_code == 200

        assert response.json() == expected_response

    async def test_get_project_statistics_returns_files_and_transfer_activity_statistics_filtered_by_zone(
        self, fake, client, metadata_item_factory, item_activity_factory
    ):
        project_code = metadata_item_factory.generate_container_code()
        zone = metadata_item_factory.generate_zone()
        other_zone = zone + 1
        time = datetime.now(tz=timezone.utc)
        created_metadata_item = await metadata_item_factory.create(
            container_code=project_code, created_time=time, type_=MetadataItemType.FILE, zone=zone
        )
        await metadata_item_factory.bulk_create(
            2, container_code=project_code, created_time=time, type_=MetadataItemType.FILE, zone=other_zone
        )
        await item_activity_factory.create(
            container_code=project_code, activity_time=time, activity_type=ItemActivityType.DOWNLOAD, zone=zone
        )
        await item_activity_factory.bulk_create(
            2, container_code=project_code, activity_time=time, activity_type=ItemActivityType.DOWNLOAD, zone=other_zone
        )

        expected_response = {
            'files': {
                'total_count': 1,
                'total_size': created_metadata_item.size,
            },
            'activity': {
                'today_uploaded': 0,
                'today_downloaded': 1,
            },
        }

        response = await client.get(
            f'/v1/project-files/{project_code}/statistics', params={'time_zone': '+00:00', 'zone': zone}
        )

        assert response.status_code == 200

        assert response.json() == expected_response

    async def test_get_project_file_activity_returns_project_activity_datasets_grouped_by_day(
        self, client, item_activity_factory
    ):
        created_item_activity = await item_activity_factory.create()
        from_date = created_item_activity.activity_time.isoformat()
        to_date = (created_item_activity.activity_time + timedelta(days=1)).isoformat()

        expected_response = {'data': {created_item_activity.activity_time.strftime('%Y-%m-%d'): 1}}

        response = await client.get(
            f'/v1/project-files/{created_item_activity.container_code}/activity',
            params={
                'type': created_item_activity.activity_type.value,
                'from': from_date,
                'to': to_date,
                'time_zone': '+00:00',
            },
        )

        assert response.status_code == 200

        assert response.json() == expected_response

    async def test_get_project_file_activity_returns_project_activity_datasets_grouped_by_day_and_filtered_by_user(
        self, client, item_activity_factory
    ):
        created_item_activity = await item_activity_factory.create()
        await item_activity_factory.bulk_create(
            2,
            container_code=created_item_activity.container_code,
            activity_time=created_item_activity.activity_time,
            activity_type=created_item_activity.activity_type,
        )
        from_date = created_item_activity.activity_time.isoformat()
        to_date = (created_item_activity.activity_time + timedelta(days=1)).isoformat()

        expected_response = {'data': {created_item_activity.activity_time.strftime('%Y-%m-%d'): 1}}

        response = await client.get(
            f'/v1/project-files/{created_item_activity.container_code}/activity',
            params={
                'type': created_item_activity.activity_type.value,
                'from': from_date,
                'to': to_date,
                'time_zone': '+00:00',
                'user': created_item_activity.user,
            },
        )

        assert response.status_code == 200

        assert response.json() == expected_response
