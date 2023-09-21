# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

METADATA_ITEM_INDEX_MAPPINGS = {
    'properties': {
        'status': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'attributes': {'type': 'nested', 'properties': {'name': {'type': 'keyword'}, 'value': {'type': 'keyword'}}},
        'container_code': {'type': 'keyword'},
        'container_type': {'type': 'keyword'},
        'created_time': {'type': 'date', 'format': 'epoch_second'},
        'extended_id': {'type': 'keyword'},
        'id': {'type': 'keyword'},
        'last_updated_time': {'type': 'date', 'format': 'epoch_second'},
        'location_uri': {'type': 'keyword'},
        'name': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'owner': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'parent': {'type': 'keyword'},
        'parent_path': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}, 'analyzer': 'path_analyzer'},
        'restore_path': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}, 'analyzer': 'path_analyzer'},
        'size': {'type': 'long'},
        'storage_id': {'type': 'keyword'},
        'system_tags': {'type': 'keyword'},
        'tags': {'type': 'keyword'},
        'template_id': {'type': 'keyword'},
        'template_name': {'type': 'keyword'},
        'type': {'type': 'keyword'},
        'version': {'type': 'keyword'},
        'zone': {'type': 'byte'},
    },
}
