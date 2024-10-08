# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from fastapi import Query

from search.components.item_activity.models import ActivityGroupBy
from search.components.item_activity.models import ItemActivityType
from search.components.metadata_item.models import SizeGroupBy
from search.components.parameters import QueryParameters

TIME_ZONE_REGEX = r'^[-+][0-9]{2}:[0-9]{2}$'


class ProjectFilesTimeRangeParameters(QueryParameters):
    """Query parameters for querying project files within time range."""

    from_date: datetime = Query(alias='from')
    to_date: datetime = Query(alias='to')
    time_zone: str = Query(default='+00:00', regex=TIME_ZONE_REGEX)


class ProjectFilesSizeParameters(ProjectFilesTimeRangeParameters):
    """Query parameters for querying project files size."""

    group_by: SizeGroupBy = Query(default=SizeGroupBy.MONTH)


class ProjectFilesActivityParameters(ProjectFilesTimeRangeParameters):
    """Query parameters for querying project files activity."""

    group_by: ActivityGroupBy = Query(default=ActivityGroupBy.DAY)
    activity_type: ItemActivityType = Query(default=ItemActivityType.DOWNLOAD, alias='type')
    user: str | None = Query(default=None)


class ProjectFilesStatisticsParameters(QueryParameters):
    """Query parameters for querying project files statistics."""

    parent_path: str | None = Query(default=None)
    zone: int | None = Query(default=None)
    time_zone: str = Query(default='+00:00', regex=TIME_ZONE_REGEX)
