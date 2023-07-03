[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Workflow](https://github.com/MishaVyb/application-builder/actions/workflows/gitlab-ci-cd.yml/badge.svg)](https://github.com/MishaVyb/application-builder/actions/workflows/gitlab-ci-cd.yml)

# Application Builder

![Drawing 2023-07-03 11 32 45 excalidraw](https://github.com/MishaVyb/application-builder/assets/103563736/2f2e3fa0-c337-4962-905c-47892e7c5236)

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
git clone git@github.com:MishaVyb/application-builder.git
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

- Documentation
```
http://localhost:8080/docs
```

# Tests
- Install develop requirements
```sh
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements_dev.txt
```

- Run all tests
```sh
pytest -v
```

- Also you may run `test_get_tasks_200` to check getting tasks for all builds or for specific one.
```sh
pytest -v -s -k 'test_get_tasks_200'
pytest -v -s -k 'test_get_tasks_200 and forward_interest'  # check only 'forward_interest' build
```

```sh
tests/routes/test_tasks.py::test_get_tasks_200[forward_interest]
INFO - Initialize: Application build system. Settings: {'BASEDIR': PosixPath('/Users/vybornyy/dev/application-builder'),
 'BUILDS_FILE_PATH': PosixPath('/Users/vybornyy/dev/application-builder/builds/builds.yaml'),
 'DEBUG': False,
 'LOG_LEVEL': 20,
 'TASKS_FILE_PATH': PosixPath('/Users/vybornyy/dev/application-builder/builds/tasks.yaml')}.
INFO - Start [App: init].
INFO - Stop [App: init]. It takes: 0.08576798439025879.
INFO - Resolve: forward_interest
INFO - Result: ['build_teal_leprechauns', 'enable_yellow_centaurs', 'bring_olive_centaurs', 'coloring_white_centaurs', 'create_teal_centaurs', 'design_lime_centaurs', 'train_purple_centaurs', 'upgrade_navy_centaurs', 'create_maroon_centaurs', 'bring_blue_centaurs', 'read_yellow_centaurs', 'create_olive_centaurs', 'coloring_aqua_centaurs', 'coloring_aqua_golems', 'coloring_navy_golems', 'map_black_leprechauns', 'upgrade_white_leprechauns', 'map_olive_leprechauns', 'enable_lime_leprechauns', 'create_aqua_humans', 'enable_olive_humans', 'build_maroon_humans', 'write_silver_humans', 'write_white_humans', 'create_purple_humans', 'train_white_humans', 'write_teal_humans', 'enable_silver_humans', 'bring_blue_ogres', 'design_white_ogres', 'train_green_ogres', 'upgrade_aqua_ogres', 'write_silver_ogres', 'enable_fuchsia_ogres', 'bring_green_ogres', 'build_yellow_ogres', 'create_maroon_ogres', 'design_green_ogres', 'upgrade_navy_ogres', 'write_blue_ogres', 'write_fuchsia_golems'].
PASSED
```

