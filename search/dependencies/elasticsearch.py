# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search.config import Settings
from search.config import get_settings


async def get_elasticsearch_client(settings: Settings = Depends(get_settings)) -> AsyncElasticsearch:
    """Create a FastAPI callable dependency for async Elasticsearch client instance."""

    client = AsyncElasticsearch(settings.ELASTICSEARCH_URI)

    try:
        yield client
    finally:
        await client.close()
