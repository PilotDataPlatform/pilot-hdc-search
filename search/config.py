# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'search'
    VERSION: str = '2.1.0'
    HOST: str = '127.0.0.1'
    PORT: int = 5064
    WORKERS: int = 1
    RELOAD: bool = False

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    ELASTICSEARCH_URI: str = 'http://127.0.0.1:9201'

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
