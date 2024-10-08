# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter
from fastapi import Depends

from search.components.item_activity.crud import ItemActivityCRUD
from search.components.item_activity.dependencies import get_item_activity_crud
from search.components.item_activity.parameters import ItemActivityFilterParameters
from search.components.item_activity.parameters import ItemActivitySortByFields
from search.components.item_activity.schemas import ItemActivityListResponseSchema
from search.components.parameters import PageParameters
from search.components.parameters import SortParameters

router = APIRouter(prefix='/item-activity-logs', tags=['Item Activity'])


@router.get('/', summary='List project items activity logs.', response_model=ItemActivityListResponseSchema)
async def list_item_activity_logs(
    filter_parameters: ItemActivityFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(ItemActivitySortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    item_activity_crud: ItemActivityCRUD = Depends(get_item_activity_crud),
) -> ItemActivityListResponseSchema:
    """List item activity logs."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    page = await item_activity_crud.list(pagination, sorting, filtering)
    response = ItemActivityListResponseSchema.from_page(page)

    return response
