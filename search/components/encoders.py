# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime


def datetime_to_timestamp(value: datetime) -> int:
    """Convert datetime into timestamp (epoch seconds)."""

    return int(value.timestamp())


datetime_as_timestamp_encoder = {
    datetime: datetime_to_timestamp,
}
