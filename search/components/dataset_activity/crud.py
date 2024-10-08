# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

from search.components.crud import CRUD
from search.components.dataset_activity.index import DATASET_ACTIVITY_INDEX_MAPPINGS
from search.components.dataset_activity.models import DatasetActivity
from search.components.dataset_activity.models import DatasetAndItemActivity
from search.components.dataset_activity.models import DatasetAndItemActivityIndex


class DatasetActivityCRUD(CRUD):
    """CRUD for managing dataset activity logs."""

    index = 'datasets-activity-logs'
    index_mappings = DATASET_ACTIVITY_INDEX_MAPPINGS
    model = DatasetActivity


class DatasetAndItemActivityCRUD(CRUD):
    """CRUD for managing combined dataset and item activity logs."""

    index = ['datasets-activity-logs', 'items-activity-logs']
    model = DatasetAndItemActivity
    index_to_model_index_mapping = {
        'datasets-activity-logs': DatasetAndItemActivityIndex.DATASET,
        'items-activity-logs': DatasetAndItemActivityIndex.ITEM,
    }

    def _parse_document(self, document: dict[str, Any]) -> DatasetAndItemActivity:
        """Parse elasticsearch document source into a model instance."""

        document['_source']['pk'] = document['_id']
        document['_source']['index'] = self.index_to_model_index_mapping[document['_index']]

        return self.model.parse_obj(document['_source'])
