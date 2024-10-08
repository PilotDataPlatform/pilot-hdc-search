# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search.components.dataset_activity.crud import DatasetAndItemActivityCRUD
from search.dependencies import get_elasticsearch_client


def get_dataset_and_item_activity_crud(
    elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client),
) -> DatasetAndItemActivityCRUD:
    """Return an instance of DatasetAndItemActivityCRUD as a dependency."""

    return DatasetAndItemActivityCRUD(elasticsearch_client)
