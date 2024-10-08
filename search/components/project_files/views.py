# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timezone
from typing import Union

from fastapi import APIRouter
from fastapi import Depends

from search.components.item_activity.crud import ItemActivityCRUD
from search.components.item_activity.dependencies import get_item_activity_crud
from search.components.item_activity.filtering import ItemActivityProjectFileActivityFiltering
from search.components.metadata_item.crud import MetadataItemCRUD
from search.components.metadata_item.dependencies import get_metadata_item_crud
from search.components.metadata_item.filtering import MetadataItemProjectSizeUsageFiltering
from search.components.project_files.parameters import ProjectFilesActivityParameters
from search.components.project_files.parameters import ProjectFilesSizeParameters
from search.components.project_files.parameters import ProjectFilesStatisticsParameters
from search.components.project_files.schemas import ProjectFilesActivityResponseSchema
from search.components.project_files.schemas import ProjectFilesSizeResponseSchema
from search.components.project_files.schemas import ProjectFilesSizeSchema
from search.components.project_files.schemas import ProjectFilesStatisticsResponseSchema
from search.components.project_files.schemas import ProjectFilesTodayActivity
from search.components.project_files.schemas import ProjectFilesTotalStatistics

router = APIRouter(prefix='/project-files', tags=['Project Files'])


@router.get(
    '/{project_code}/size', summary='Get storage usage in the project.', response_model=ProjectFilesSizeResponseSchema
)
async def get_project_size_usage(
    project_code: str,
    parent_path: Union[str, None] = None,
    parameters: ProjectFilesSizeParameters = Depends(),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
) -> ProjectFilesSizeResponseSchema:
    """Get storage usage in a project for the period."""

    filtering = MetadataItemProjectSizeUsageFiltering(
        project_code=project_code, parent_path=parent_path, from_date=parameters.from_date, to_date=parameters.to_date
    )

    project_size_usage = await metadata_item_crud.get_project_size_usage(
        filtering, parameters.time_zone, parameters.group_by
    )

    return ProjectFilesSizeResponseSchema(data=ProjectFilesSizeSchema(**project_size_usage.dict()))


@router.get(
    '/{project_code}/statistics',
    summary='Get files and transfer activity statistics in the project.',
    response_model=ProjectFilesStatisticsResponseSchema,
)
async def get_project_statistics(
    project_code: str,
    parameters: ProjectFilesStatisticsParameters = Depends(),
    metadata_item_crud: MetadataItemCRUD = Depends(get_metadata_item_crud),
    item_activity_crud: ItemActivityCRUD = Depends(get_item_activity_crud),
) -> ProjectFilesStatisticsResponseSchema:
    """Get files and transfer activity statistics in a project for the period."""

    now = datetime.now(tz=timezone.utc)

    statistics = await metadata_item_crud.get_project_statistics(project_code, parameters.parent_path, parameters.zone)
    transfer_statistics = await item_activity_crud.get_project_transfer_statistics(
        project_code, now, parameters.time_zone, parameters.parent_path, parameters.zone
    )

    return ProjectFilesStatisticsResponseSchema(
        files=ProjectFilesTotalStatistics(
            total_count=statistics.count,
            total_size=statistics.size,
        ),
        activity=ProjectFilesTodayActivity(
            today_uploaded=transfer_statistics.uploaded,
            today_downloaded=transfer_statistics.downloaded,
        ),
    )


@router.get(
    '/{project_code}/activity',
    summary='Get file activity in the project.',
    response_model=ProjectFilesActivityResponseSchema,
)
async def get_project_file_activity(
    project_code: str,
    parameters: ProjectFilesActivityParameters = Depends(),
    item_activity_crud: ItemActivityCRUD = Depends(get_item_activity_crud),
) -> ProjectFilesActivityResponseSchema:
    """Get file activity in a project for the period."""

    filtering = ItemActivityProjectFileActivityFiltering(
        project_code=project_code,
        activity_type=parameters.activity_type,
        from_date=parameters.from_date,
        to_date=parameters.to_date,
        user=parameters.user,
    )

    project_file_activity = await item_activity_crud.get_project_file_activity(
        filtering, parameters.time_zone, parameters.group_by
    )

    return ProjectFilesActivityResponseSchema(data=project_file_activity)
