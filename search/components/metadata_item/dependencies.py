# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search.components.metadata_item.crud import MetadataItemCRUD
from search.dependencies import get_elasticsearch_client


def get_metadata_item_crud(
    elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client),
) -> MetadataItemCRUD:
    """Return an instance of MetadataItemCRUD as a dependency."""

    return MetadataItemCRUD(elasticsearch_client)
