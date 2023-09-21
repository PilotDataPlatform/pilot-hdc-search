# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import time
from datetime import timezone

import faker
import pytest


class Faker(faker.Faker):
    def date_this_year_midnight_time(self) -> datetime:
        return datetime.combine(self.date_this_year(), time(tzinfo=timezone.utc))

    def past_datetime_utc(self) -> datetime:
        return self.past_datetime(tzinfo=timezone.utc)


@pytest.fixture(scope='session')
def fake(pytestconfig) -> Faker:
    seed = pytestconfig.getoption('random_order_seed', '0').lstrip('default:')

    fake = Faker()
    fake.seed_instance(seed=seed)
    fake.unique.clear()

    yield fake
