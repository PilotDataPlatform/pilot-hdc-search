# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timezone

from search.components.encoders import datetime_to_timestamp


class TestEncoders:
    def test_datetime_to_timestamp_converts_utc_datetime_into_seconds_timestamp(self):
        assert datetime_to_timestamp(datetime(1970, 1, 1, 0, 1, tzinfo=timezone.utc)) == 60
