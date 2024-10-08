# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from search.components.crud import CRUD


class TestCRUD:
    async def test_create_index_creates_index_using_index_name_defined_in_index_attribute(self, es_client, fake):
        class CustomCRUD(CRUD):
            index = f'test-{fake.pystr().lower()}'

        crud = CustomCRUD(es_client)

        await crud.create_index()

        is_exists = await crud.is_index_exists()
        assert is_exists is True
