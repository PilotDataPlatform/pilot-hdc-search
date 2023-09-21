# Search Service

[![Python](https://img.shields.io/badge/python-3.10-brightgreen.svg)](https://www.python.org/)

## About

Service for performing searches.

### Start

1. Install [Docker](https://www.docker.com/get-started/).
2. Start container with search application.

       docker compose up

3. Visit http://127.0.0.1:5064/v1/api-doc for API documentation.

### Development

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Install dependencies.

       poetry install

3. Add environment variables into `.env`.
4. Run application.

       poetry run python -m search

## Acknowledgements
The development of the HealthDataCloud open source software was supported by the EBRAINS research infrastructure, funded from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3) and H2020 Research and Innovation Action Grant Interactive Computing E-Infrastructure for the Human Brain Project ICEI 800858.
