# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from search.components.item_activity.models import ItemActivity
from search.components.item_activity.views import router as item_activity_router

__all__ = ['ItemActivity', 'item_activity_router']
