# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Type

from common import LoggerFactory
from elasticsearch import AsyncElasticsearch

from search.components.crud import CRUD
from search.config import get_settings

settings = get_settings()
_logger = LoggerFactory(
    name=__name__,
    level_default=settings.LOG_LEVEL_DEFAULT,
    level_file=settings.LOG_LEVEL_FILE,
    level_stdout=settings.LOG_LEVEL_STDOUT,
    level_stderr=settings.LOG_LEVEL_STDERR,
).get_logger()


class IndexChecker:
    """Check if required indexes are available in the elasticsearch and create them if not."""

    def __init__(self, elasticsearch_uri: str) -> None:
        self.client = AsyncElasticsearch(elasticsearch_uri)

    async def check_crud(self, crud: CRUD) -> None:
        """Check index of one CRUD."""

        _logger.info(f'Checking if index "{crud.index}" exists.')
        is_exists = await crud.is_index_exists()
        _logger.info(f'Existence check result for index "{crud.index}" is "{is_exists}".')

        if not is_exists:
            _logger.info(f'Creating index "{crud.index}" for CRUD "{crud}".')
            await crud.create_index()
            _logger.info(f'The index "{crud.index}" has been successfully created.')

    async def check_cruds(self, cruds: list[Type[CRUD]]) -> None:
        """Check indexes for a list of CRUDs."""

        _logger.info(f'Start checking for the existence of indexes for the CRUDs: {cruds}.')
        try:
            for crud in cruds:
                await self.check_crud(crud(self.client))
        except Exception:
            _logger.exception('An exception occurred while performing CRUDs indexes check.')
        else:
            _logger.info('The indexes check is successfully completed.')
        finally:
            await self.client.close()
