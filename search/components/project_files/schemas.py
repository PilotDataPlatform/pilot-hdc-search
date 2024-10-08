# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from search.components.schemas import BaseSchema


class ProjectFilesSizeDatasetSchema(BaseSchema):
    """General project files size datasets schema."""

    label: int
    values: list[int]


class ProjectFilesSizeSchema(BaseSchema):
    """General project files size schema."""

    labels: list[str]
    datasets: list[ProjectFilesSizeDatasetSchema]


class ProjectFilesSizeResponseSchema(BaseSchema):
    """Default schema for project files size response."""

    data: ProjectFilesSizeSchema


class ProjectFilesTotalStatistics(BaseSchema):
    """Project files total statistics schema."""

    total_count: int
    total_size: int


class ProjectFilesTodayActivity(BaseSchema):
    """Project files today's activity schema."""

    today_uploaded: int
    today_downloaded: int


class ProjectFilesStatisticsResponseSchema(BaseSchema):
    """Default schema for project files statistics response."""

    files: ProjectFilesTotalStatistics
    activity: ProjectFilesTodayActivity


class ProjectFilesActivityResponseSchema(BaseSchema):
    """Default schema for project files activity response."""

    data: dict[str, int]
