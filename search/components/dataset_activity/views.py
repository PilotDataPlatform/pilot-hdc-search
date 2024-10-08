# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter
from fastapi import Depends

from search.components.dataset_activity.crud import DatasetAndItemActivityCRUD
from search.components.dataset_activity.dependencies import get_dataset_and_item_activity_crud
from search.components.dataset_activity.parameters import DatasetActivitySortByFields
from search.components.dataset_activity.parameters import DatasetAndItemActivityFilterParameters
from search.components.dataset_activity.schemas import DatasetAndItemActivityListResponseSchema
from search.components.parameters import PageParameters
from search.components.parameters import SortParameters

router = APIRouter(prefix='/dataset-activity-logs', tags=['Dataset Activity'])


@router.get(
    '/', summary='List all dataset and items activity logs.', response_model=DatasetAndItemActivityListResponseSchema
)
async def list_dataset_and_item_activity_logs(
    filter_parameters: DatasetAndItemActivityFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(DatasetActivitySortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    dataset_and_item_activity_crud: DatasetAndItemActivityCRUD = Depends(get_dataset_and_item_activity_crud),
) -> DatasetAndItemActivityListResponseSchema:
    """List dataset and item activity logs."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    page = await dataset_and_item_activity_crud.list(pagination, sorting, filtering)
    response = DatasetAndItemActivityListResponseSchema.from_page(page)

    return response
