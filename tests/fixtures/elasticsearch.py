# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest
from elasticsearch import AsyncElasticsearch
from testcontainers.elasticsearch import ElasticSearchContainer


@pytest.fixture(scope='session')
def elasticsearch_uri(get_service_image) -> str:
    elasticsearch_image = get_service_image('elasticsearch')

    with ElasticSearchContainer(elasticsearch_image) as es_container:
        yield es_container.get_url()


@pytest.fixture(scope='session')
async def es_client(settings) -> AsyncElasticsearch:
    client = AsyncElasticsearch(settings.ELASTICSEARCH_URI)

    try:
        yield client
    finally:
        await client.close()
