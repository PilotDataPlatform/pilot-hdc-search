# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any


class SearchQuery:
    """Build elastic search query."""

    def __init__(self) -> None:
        self.must = []
        self.nested = {}

    def match_text(self, field: str, value: str) -> None:
        """Perform full-text search using "match" or "wildcard" query."""

        query_type = 'match'
        query_value = {field: value}

        is_wildcard = '%' in value
        if is_wildcard:
            query_type = 'wildcard'
            query_value = {
                field: {
                    'value': value.replace('%', '*'),
                    # This doesn't work with German umlauts (ä != Ä). Consider trying german_normalization.
                    'case_insensitive': True,
                }
            }

        self.must.append({query_type: query_value})

    def match_range(self, field: str, **kwds: Any) -> None:
        self.must.append({'range': {field: kwds}})

    def match_term(self, field: str, value: str | int | bool) -> None:
        self.must.append({'term': {field: value}})

    def match_multiple_terms(self, field: str, value: list[str | int]) -> None:
        self.must.append({'terms': {field: value}})

    def init_nested(self, nested_field: str) -> None:
        self.nested = {
            'nested': {
                'path': nested_field,
                'query': {
                    'bool': {'must': [], 'should': [], 'minimum_should_match': 0},
                },
            }
        }

    def match_nested_exact(self, nested_field: str, field: str, accepted_values: list) -> None:
        for value in accepted_values:
            self.nested['nested']['query']['bool']['should'].append({'match': {f'{nested_field}.{field}': value}})
        self.nested['nested']['query']['bool']['minimum_should_match'] = 1

    def match_nested_contains(self, nested_field: str, field: str, value: str) -> None:
        value = f'*{value}*'
        self.nested['nested']['query']['bool']['must'].append({'wildcard': {f'{nested_field}.{field}': value}})

    def build(self) -> dict[str, Any]:
        if not self.must:
            return {'match_all': {}}

        if self.nested:
            self.must.append(self.nested)

        es_query = {'bool': {'must': self.must}}
        return es_query
