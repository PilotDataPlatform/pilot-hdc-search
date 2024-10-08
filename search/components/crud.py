# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import os
from typing import Any
from typing import ClassVar

from elasticsearch import AsyncElasticsearch

from search.components.filtering import Filtering
from search.components.index import INDEX_SETTINGS
from search.components.models import Model
from search.components.pagination import Page
from search.components.pagination import PageType
from search.components.pagination import Pagination
from search.components.schemas import BaseSchema
from search.components.search_query import SearchQuery
from search.components.sorting import Sorting


class CRUD:
    """Base CRUD class for managing elasticsearch documents."""

    index: ClassVar[str | list[str]]
    index_settings: ClassVar[dict[str, Any]] = INDEX_SETTINGS
    index_mappings: ClassVar[dict[str, Any]] = {}
    model: ClassVar[Model]

    client: AsyncElasticsearch

    def __init__(self, client: AsyncElasticsearch) -> None:
        self.client = client

    def __str__(self) -> str:
        return self.__class__.__name__

    def _generate_pk(self) -> str:
        """Generate random primary key for a document."""

        return os.urandom(10).hex()

    def _parse_document(self, document: dict[str, Any]) -> Model:
        """Parse elasticsearch document source into a model instance."""
        document['_source']['pk'] = document['_id']
        return self.model.parse_obj(document['_source'])

    def _parse_documents(self, documents: list[dict[str, Any]]) -> list[Model]:
        """Parse a list of elasticsearch document sources into a list of model instances."""

        return [self._parse_document(document) for document in documents]

    async def _create_one(self, **kwds: Any) -> dict[str, Any]:
        """Use elasticsearch client to create one document."""

        return await self.client.create(index=self.index, **kwds)

    async def _retrieve_one(self, **kwds: Any) -> dict[str, Any]:
        """Use elasticsearch client to retrieve one document."""

        return await self.client.get(index=self.index, **kwds)

    async def _search(self, **kwds: Any) -> dict[str, Any]:
        """Use elasticsearch client to execute a search query and get back search hits."""

        return await self.client.search(index=self.index, **kwds)

    async def create_index(self) -> None:
        """Create a new index."""

        await self.client.indices.create(index=self.index, mappings=self.index_mappings, settings=self.index_settings)

    async def is_index_exists(self) -> bool:
        """Check if index exists."""

        return await self.client.indices.exists(index=self.index)

    async def create(self, model: BaseSchema, **kwds: Any) -> Model:
        """Create a new entry."""

        document = await self._create_one(id=self._generate_pk(), document=model.json(ensure_ascii=False), **kwds)

        entry = await self.retrieve_by_pk(document['_id'])

        return entry

    async def retrieve_by_pk(self, pk: str) -> Model:
        """Get an existing entry by primary key."""

        document = await self._retrieve_one(id=pk)

        entry = self._parse_document(document)

        return entry

    async def _list(self, **kwds: Any) -> dict[str, Any]:
        """Get a list of entries by executing a search."""
        return await self._search(**kwds)

    async def _paginate_list_result(self, result: dict[str, Any], pagination: Pagination) -> Page:
        """Create a response page from list result."""
        count = result['hits']['total']['value']
        entries = self._parse_documents(result['hits']['hits'])

        return Page(pagination=pagination, count=count, entries=entries)

    async def list(
        self, pagination: Pagination, sorting: Sorting | None = None, filtering: Filtering | None = None
    ) -> PageType:
        """Get all existing entries with pagination, sorting and filtering support."""
        search_query = SearchQuery()

        sort = None
        if sorting:
            sort = sorting.apply()

        if filtering or not hasattr(filtering, 'container_type'):
            filtering.apply(search_query)

        query = search_query.build()

        result = await self._list(query=query, sort=sort, size=pagination.size, from_=pagination.from_)

        return await self._paginate_list_result(result, pagination)
