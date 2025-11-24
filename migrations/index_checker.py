# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from common import configure_logging
from elasticsearch import AsyncElasticsearch

from search.components.crud import CRUD
from search.config import get_settings
from search.logger import logger

settings = get_settings()
configure_logging(settings.LOGGING_LEVEL, settings.LOGGING_FORMAT)


class IndexChecker:
    """Check if required indexes are available in the elasticsearch and create them if not."""

    def __init__(self, elasticsearch_uri: str) -> None:
        self.client = AsyncElasticsearch(elasticsearch_uri)

    async def check_crud(self, crud: CRUD) -> None:
        """Check index of one CRUD."""

        logger.info(f'Checking if index "{crud.index}" exists.')
        is_exists = await crud.is_index_exists()
        logger.info(f'Existence check result for index "{crud.index}" is "{is_exists}".')

        if not is_exists:
            logger.info(f'Creating index "{crud.index}" for CRUD "{crud}".')
            await crud.create_index()
            logger.info(f'The index "{crud.index}" has been successfully created.')

    async def check_cruds(self, cruds: list[type[CRUD]]) -> None:
        """Check indexes for a list of CRUDs."""

        logger.info(f'Start checking for the existence of indexes for the CRUDs: {cruds}.')
        try:
            for crud in cruds:
                await self.check_crud(crud(self.client))
        except Exception:
            logger.exception('An exception occurred while performing CRUDs indexes check.')
        else:
            logger.info('The indexes check is successfully completed.')
        finally:
            await self.client.close()
