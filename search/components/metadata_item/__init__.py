# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from search.components.metadata_item.models import MetadataItem
from search.components.metadata_item.views import router as metadata_item_router

__all__ = [
    'MetadataItem',
    'metadata_item_router',
]
