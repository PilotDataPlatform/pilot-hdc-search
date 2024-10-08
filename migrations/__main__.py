# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio

from migrations.index_checker import IndexChecker
from search.components.dataset_activity.crud import DatasetActivityCRUD
from search.components.item_activity.crud import ItemActivityCRUD
from search.components.metadata_item.crud import MetadataItemCRUD
from search.config import get_settings

if __name__ == '__main__':
    settings = get_settings()
    index_checker = IndexChecker(settings.ELASTICSEARCH_URI)
    asyncio.run(index_checker.check_cruds([MetadataItemCRUD, ItemActivityCRUD, DatasetActivityCRUD]))
