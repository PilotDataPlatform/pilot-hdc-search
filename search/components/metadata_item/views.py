# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter
from fastapi import Depends

from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.dependencies import get_metadata_item_crud
from search.components.metadata_item.parameters import MetadataItemFilterParameters
from search.components.metadata_item.parameters import MetadataItemSortByFields
from search.components.metadata_item.schemas import MetadataItemListResponseSchema
from search.components.parameters import PageParameters
from search.components.parameters import SortParameters

router = APIRouter(prefix='/metadata-items', tags=['Metadata Items'])


@router.get('/', summary='List all metadata items.', response_model=MetadataItemListResponseSchema)
async def list_metadata_items(
    filter_parameters: MetadataItemFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(MetadataItemSortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
) -> MetadataItemListResponseSchema:
    """List metadata items."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()
    page = await metadata_item_crud.list(pagination, sorting, filtering)

    response = MetadataItemListResponseSchema.from_page(page)

    return response
