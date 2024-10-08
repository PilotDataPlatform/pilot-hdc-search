# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

DATASET_ACTIVITY_INDEX_MAPPINGS = {
    'properties': {
        'activity_time': {'type': 'date', 'format': 'epoch_second'},
        'activity_type': {'type': 'keyword'},
        'changes': {
            'type': 'nested',
            'properties': {
                'property': {'type': 'keyword'},
                'new_value': {'type': 'keyword'},
                'old_value': {'type': 'keyword'},
            },
        },
        'container_code': {'type': 'keyword'},
        'target_name': {'type': 'keyword'},
        'user': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
        'version': {'type': 'keyword'},
    },
}
