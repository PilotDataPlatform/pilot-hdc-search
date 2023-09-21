# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

INDEX_SETTINGS = {
    'analysis': {
        'analyzer': {'path_analyzer': {'tokenizer': 'path_tokenizer'}},
        'tokenizer': {'path_tokenizer': {'type': 'path_hierarchy', 'delimiter': '.'}},
    }
}
