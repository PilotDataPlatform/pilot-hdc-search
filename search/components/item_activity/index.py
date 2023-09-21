# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

ITEM_ACTIVITY_INDEX_MAPPINGS = {
    'properties': {
        'activity_time': {'type': 'date', 'format': 'epoch_second'},
        'activity_type': {'type': 'keyword'},
        'changes': {
            'type': 'nested',
            'properties': {
                'item_property': {'type': 'keyword'},
                'new_value': {'type': 'keyword'},
                'old_value': {'type': 'keyword'},
            },
        },
        'container_code': {'type': 'keyword'},
        'container_type': {'type': 'keyword'},
        'imported_from': {'type': 'keyword'},
        'item_id': {'type': 'keyword'},
        'item_name': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'item_parent_path': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}, 'analyzer': 'path_analyzer'},
        'item_type': {'type': 'keyword'},
        'user': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'zone': {'type': 'byte'},
    },
}
