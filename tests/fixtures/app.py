# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio
from asyncio import AbstractEventLoop
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml
from fastapi import FastAPI
from httpx import AsyncClient

from search.app import create_app
from search.config import Settings
from search.config import get_settings


@pytest.fixture(scope='session')
def project_root() -> Path:
    path = Path(__file__)

    while not (path / 'pyproject.toml').is_file():
        path = path.parent

    return path


@pytest.fixture(scope='session')
def get_service_image(project_root) -> Callable[[str], str]:
    with open(project_root / 'docker-compose.yaml') as file:
        services = yaml.safe_load(file)['services']

    def get_image(service_name: str) -> str:
        return services[service_name]['image']

    yield get_image


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture(scope='session')
def settings(elasticsearch_uri) -> Settings:
    settings = Settings(ELASTICSEARCH_URI=elasticsearch_uri)
    yield settings


@pytest.fixture
def app(event_loop, settings) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    yield app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='https://') as client:
        yield client
