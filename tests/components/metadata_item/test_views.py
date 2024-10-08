# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest

from search.components.metadata_item.models import MetadataItemType
from search.components.metadata_item.parameters import MetadataItemSortByFields
from search.components.sorting import SortingOrder


class TestMetadataItemViews:
    async def test_list_metadata_items_returns_list_of_existing_metadata_items(self, client, jq, metadata_item_factory):
        created_metadata_item = await metadata_item_factory.create()

        response = await client.get('/v1/metadata-items/')

        assert response.status_code == 200

        body = jq(response)
        received_metadata_item_pk = body('.result[].pk').first()
        received_total = body('.total').first()

        assert received_metadata_item_pk == str(created_metadata_item.pk)
        assert received_total == 1

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
    async def test_list_metadata_items_returns_properly_paginated_response(
        self, items_number, page, page_size, expected_count, client, jq, metadata_item_factory
    ):
        await metadata_item_factory.bulk_create(items_number)

        response = await client.get('/v1/metadata-items/', params={'page': page, 'page_size': page_size})

        assert response.status_code == 200

        body = jq(response)
        received_metadata_item_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert len(received_metadata_item_ids) == expected_count
        assert received_total == items_number

    @pytest.mark.parametrize('sort_by', MetadataItemSortByFields.values())
    @pytest.mark.parametrize('sort_order', SortingOrder.values())
    async def test_list_metadata_items_returns_results_sorted_by_field_with_proper_order(
        self, sort_by, sort_order, client, jq, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        field_values = created_metadata_items.get_field_values(sort_by)
        if sort_by in ('created_time', 'last_updated_time'):
            field_values = [key.isoformat() for key in field_values]
        expected_values = sorted(field_values, reverse=sort_order == SortingOrder.DESC)

        response = await client.get('/v1/metadata-items/', params={'sort_by': sort_by, 'sort_order': sort_order})

        body = jq(response)
        received_values = body(f'.result[].{sort_by}').all()
        received_total = body('.total').first()

        assert received_values == expected_values
        assert received_total == 3

    @pytest.mark.parametrize(
        'name,lookup',
        [
            ('NAME', 'NAME'),
            ('NAME', '%NAME%'),
            ('NAME', '%name%'),
            ('name', '%NAME%'),
            ('nameäöüß', 'nameäöüß'),
            ('nameÄÖÜß', '%nameÄÖÜß%'),
            ('ABC-1234_name.zip', 'ABC-1234_name.zip'),
            ('ABC-1234_name.zip', '%ABC-1234_name.zip%'),
            ('name-abc', 'name-abc'),
            ('name-abc', '%name-abc%'),
            ('.name', '.name'),
            ('.name', '%.name%'),
        ],
    )
    async def test_list_metadata_items_returns_metadata_item_filtered_by_name(
        self, name, lookup, client, jq, metadata_item_factory
    ):
        created_metadata_item = await metadata_item_factory.create(name=name)

        response = await client.get('/v1/metadata-items/', params={'name': lookup})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(created_metadata_item.id)]
        assert received_total == 1

    @pytest.mark.parametrize(
        'owner,lookup',
        [
            ('owner', 'owner'),
            ('OWNER', '%OWNER%'),
            ('OWNER', '%owner%'),
            ('owner', '%OWNER%'),
        ],
    )
    async def test_list_metadata_items_returns_metadata_item_filtered_by_owner(
        self, owner, lookup, client, jq, metadata_item_factory
    ):
        created_metadata_item = await metadata_item_factory.create(owner=owner)

        response = await client.get('/v1/metadata-items/', params={'owner': lookup})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(created_metadata_item.id)]
        assert received_total == 1

    async def test_list_metadata_items_returns_metadata_item_filtered_by_name_considering_parent_path_full_text_match(
        self, client, jq, fake, metadata_item_factory
    ):
        name_folder_1 = fake.word().lower()
        name_folder_2 = f'{name_folder_1}-suffix'
        name_folder_3 = f'prefix-{name_folder_1}'
        name_folders = [name_folder_1, name_folder_2, name_folder_3]
        file_name = fake.file_name().lower()
        zone = metadata_item_factory.generate_zone()
        container_code = metadata_item_factory.generate_container_code()

        parent_metadata_items = await metadata_item_factory.create_name_folders(
            name_folders, zone=zone, container_code=container_code
        )
        created_metadata_items = await metadata_item_factory.create_file_for_parents(
            parent_metadata_items, zone=zone, name=file_name, container_code=container_code
        )
        expected_metadata_item_ids = created_metadata_items[0:1].get_field_values('id', str)

        response = await client.get('/v1/metadata-items/', params={'name': file_name, 'parent_path': name_folder_1})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == expected_metadata_item_ids
        assert received_total == 1

    async def test_list_metadata_items_returns_metadata_item_filtered_by_name_considering_parent_path_prefix_match(
        self, client, jq, fake, metadata_item_factory
    ):
        name_folder_1 = fake.word().lower()
        name_folder_2 = f'{name_folder_1}-suffix'
        name_folder_3 = f'prefix-{name_folder_1}'
        name_folders = [name_folder_1, name_folder_2, name_folder_3]
        file_name = fake.file_name().lower()
        zone = metadata_item_factory.generate_zone()
        container_code = metadata_item_factory.generate_container_code()

        parent_metadata_items = await metadata_item_factory.create_name_folders(
            name_folders, zone=zone, container_code=container_code
        )
        created_metadata_items = await metadata_item_factory.create_file_for_parents(
            parent_metadata_items, zone=zone, name=file_name, container_code=container_code
        )
        expected_metadata_item_ids = created_metadata_items[::2].get_field_values('id', str)

        response = await client.get(
            '/v1/metadata-items/', params={'name': file_name, 'parent_path': f'%{name_folder_1}'}
        )

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == expected_metadata_item_ids
        assert received_total == 2

    async def test_list_metadata_items_returns_metadata_item_filtered_by_name_considering_parent_path_suffix_match(
        self, client, jq, fake, metadata_item_factory
    ):
        name_folder_1 = fake.word().lower()
        name_folder_2 = f'{name_folder_1}-suffix'
        name_folder_3 = f'prefix-{name_folder_1}'
        name_folders = [name_folder_1, name_folder_2, name_folder_3]
        file_name = fake.file_name().lower()
        zone = metadata_item_factory.generate_zone()
        container_code = metadata_item_factory.generate_container_code()

        parent_metadata_items = await metadata_item_factory.create_name_folders(
            name_folders, zone=zone, container_code=container_code
        )
        created_metadata_items = await metadata_item_factory.create_file_for_parents(
            parent_metadata_items, zone=zone, name=file_name, container_code=container_code
        )
        expected_metadata_item_ids = created_metadata_items[0:2].get_field_values('id', str)

        response = await client.get(
            '/v1/metadata-items/', params={'name': file_name, 'parent_path': f'{name_folder_1}%'}
        )

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == expected_metadata_item_ids
        assert received_total == 2

    @pytest.mark.parametrize('parameter', ['zone', 'container_code', 'container_type', 'template_id'])
    async def test_list_metadata_items_returns_metadata_item_filtered_by_parameter_match(
        self, parameter, client, jq, metadata_item_factory
    ):
        created_metadata_items = await metadata_item_factory.bulk_create(3)
        value = getattr(created_metadata_items[0], parameter)
        expected_ids = {str(item.id) for item in created_metadata_items if getattr(item, parameter) == value}

        response = await client.get('/v1/metadata-items/', params={parameter: value})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert set(received_ids) == expected_ids
        assert received_total == len(expected_ids)

    async def test_list_metadata_items_returns_metadata_items_filtered_by_created_time_parameters(
        self, client, jq, fake, metadata_item_factory
    ):
        today = datetime.now(tz=timezone.utc)
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        [
            await metadata_item_factory.create(created_time=fake.date_time_between_dates(two_weeks_ago, week_ago))
            for _ in range(2)
        ]
        metadata_item = await metadata_item_factory.create(created_time=fake.date_time_between_dates(week_ago, today))

        params = {
            'created_time_start': int(datetime.timestamp(week_ago)),
            'created_time_end': int(datetime.timestamp(today)),
        }
        response = await client.get('/v1/metadata-items/', params=params)

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    async def test_list_metadata_items_returns_metadata_items_filtered_by_size_parameters(
        self, client, jq, fake, metadata_item_factory
    ):
        size_10mb = 10 * 1024**2
        size_100mb = 100 * 1024**2
        size_1gb = 1024**3

        [await metadata_item_factory.create(size=fake.pyint(size_10mb, size_100mb)) for _ in range(2)]
        metadata_item = await metadata_item_factory.create(size=fake.pyint(size_100mb, size_1gb))

        params = {
            'size_gte': size_100mb,
            'size_lte': size_1gb,
        }
        response = await client.get('/v1/metadata-items/', params=params)

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert received_ids == [str(metadata_item.id)]
        assert received_total == 1

    @pytest.mark.parametrize('is_archived', [True, False])
    async def test_list_metadata_items_returns_metadata_items_filtered_by_value_in_is_archived_parameter(
        self, is_archived, client, jq, metadata_item_factory
    ):
        await metadata_item_factory.bulk_create(2, archived=not is_archived)
        created_metadata_items = await metadata_item_factory.bulk_create(2, archived=is_archived)
        mapping = created_metadata_items.map_by_field('id', str)
        expected_ids = list(mapping.keys())

        response = await client.get('/v1/metadata-items/', params={'is_archived': str(is_archived).lower()})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()

        assert set(received_ids) == set(expected_ids)
        assert received_total == 2

    async def test_list_metadata_items_returns_metadata_items_filtered_by_contains_attributes(
        self, client, jq, metadata_item_factory
    ):
        shared_template_id = uuid.uuid4()
        await metadata_item_factory.bulk_create(3, template_id=shared_template_id, attributes=None)

        attributes_to_filter_by = {'key1': '1', 'key2': '2'}
        expected_metadata_item = await metadata_item_factory.create(
            template_id=shared_template_id, attributes={'key1': 'value1', 'key2': 'value2'}
        )
        await metadata_item_factory.bulk_create(3, template_id=shared_template_id)

        response = await client.get(
            '/v1/metadata-items/',
            params={'template_id': shared_template_id, 'attributes': json.dumps(attributes_to_filter_by)},
        )

        assert response.status_code == 200
        body = jq(response)
        received_total = body('.total').first()
        received_id = body('.result[].id').first()
        assert received_total == 1
        assert received_id == str(expected_metadata_item.id)

    async def test_list_metadata_items_returns_metadata_items_filtered_by_exact_attributes(
        self, client, jq, metadata_item_factory
    ):
        shared_template_id = uuid.uuid4()
        await metadata_item_factory.bulk_create(3, template_id=shared_template_id)

        attributes_to_filter_by = {'key1': ['value1', 'value2', 'value3'], 'key2': 'value4'}
        valid_attributes_values = attributes_to_filter_by['key1']
        expected_metadata_items = []
        for attribute_value in valid_attributes_values:
            attributes = {'key1': attribute_value, 'key2': 'value4'}
            expected_metadata_items.append(
                await metadata_item_factory.create(template_id=shared_template_id, attributes=attributes)
            )

        response = await client.get(
            '/v1/metadata-items/',
            params={'template_id': shared_template_id, 'attributes': json.dumps(attributes_to_filter_by)},
        )

        assert response.status_code == 200
        body = jq(response)
        received_total = body('.total').first()
        assert received_total == len(valid_attributes_values)

    async def test_list_metadata_items_returns_no_metadata_items_with_invalid_attributes_param(self, client):
        invalid_attributes_to_filter_by = '"key1": "value1"'

        response = await client.get(
            '/v1/metadata-items/',
            params={'template_id': uuid.uuid4(), 'attributes': invalid_attributes_to_filter_by},
        )

        assert response.status_code == 422

    async def test_list_metadata_items_returns_metadata_item_filtered_by_tags_and_type(
        self, client, jq, metadata_item_factory
    ):
        create_file_1 = await metadata_item_factory.create(tags=['tag1'], type_=MetadataItemType.FILE)
        create_file_2 = await metadata_item_factory.create(tags=['tag2'], type_=MetadataItemType.FOLDER)
        await metadata_item_factory.create(type_=MetadataItemType.FILE, tags=['tag3'])
        await metadata_item_factory.create(type_=MetadataItemType.NAME_FOLDER)

        response = await client.get('/v1/metadata-items/', params={'tags_all': 'tag1,tag2', 'type': 'file,folder'})

        body = jq(response)
        received_ids = body('.result[].id').all()
        received_total = body('.total').first()
        assert set(received_ids) == {str(create_file_1.id), str(create_file_2.id)}
        assert received_total == 2
