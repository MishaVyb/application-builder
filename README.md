[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Workflow](https://github.com/MishaVyb/bart-bot/actions/workflows/tests.yml/badge.svg)](https://github.com/MishaVyb/bart-bot/actions/workflows/gitlab-ci-cd.yml)

# Application Builder
Builder system. Handle task dependencties for each build.

# Setup
There are three options to setup `application-builder`:
- From regestry
- Build locally
- Run developer server

## From registry
Pull image from Docker Hub and run.

```sh
docker run --publish 8080:8080 --name application-builder vybornyy/application-builder
```

> NOTE: Image builds on unix sub-system at gitlab workflow and could not work properly on your system. For example, it's not compatible with Apple Silicon/M1. It's better to build image locally, as below.

## Build locally
Or build image locally and run.

- checkout
```sh
git@github.com:MishaVyb/application-builder.git
cd application-builder
```

- build
```sh
docker build --tag application-builder .
```

- run
```sh
docker run --publish 8080:8080 --name application-builder application-builder
```

## Run developer server
Or run developer server.

- checkout
```sh
git@github.com:MishaVyb/application-builder.git
cd application-builder
```

- install requirements
```sh
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- run developer server
```sh
export PYTHONPATH=.
python app/main.py
```

# Usage

```sh
curl --request POST \
  --url http://localhost:8080/api/v1/get_tasks \
  --header 'content-type: application/json' \
  --data '{"build": "forward_interest"}'
```
