import random
from timeit import timeit

import pytest

from app.core import logger, settings
from app.schemas.builds import BuildSchema, BuildsSchema
from app.schemas.tasks import TaskSchema, TasksSchema


@pytest.mark.parametrize(
    ['build', 'tasks', 'expected'],
    argvalues=[
        # [001] simple test
        pytest.param(
            BuildSchema(name='test build', tasks=['task A', 'task B']),
            TasksSchema(
                tasks=[
                    TaskSchema(name='task A', dependencies=['task C', 'task B']),
                    TaskSchema(name='task B', dependencies=['task C']),
                    TaskSchema(name='task C', dependencies=[]),
                ]
            ),
            ['task B', 'task A'],  # expected order
            id='[001] simple test',
        ),
        # [002] hard test
        pytest.param(
            BuildSchema(name='test build', tasks=['task I', 'task A', 'task B', 'task F']),
            TasksSchema(
                tasks=[
                    # build tasks:
                    TaskSchema(name='task I', dependencies=[]),
                    TaskSchema(name='task A', dependencies=['task Q', 'task Y']),
                    TaskSchema(name='task B', dependencies=['task C', 'task D', 'task E']),
                    TaskSchema(name='task F', dependencies=['task B']),
                    # sub-tasks:
                    TaskSchema(name='task Q', dependencies=[]),
                    TaskSchema(name='task Y', dependencies=['task C']),
                    TaskSchema(name='task C', dependencies=[]),
                    TaskSchema(name='task D', dependencies=[]),
                    TaskSchema(name='task E', dependencies=['task Q']),
                ]
            ),
            ['task I', 'task A', 'task B', 'task F'],  # expected order
            id='[002] hard test',
        ),
        # [003] 2 tasks with equal resolved deps len - ordered by name
        pytest.param(
            BuildSchema(name='test build', tasks=['task I', 'task A', 'task B', 'task F']),
            TasksSchema(
                tasks=[
                    # build tasks:
                    TaskSchema(name='task I', dependencies=[]),
                    TaskSchema(name='task A', dependencies=['task Q', 'task Y']),
                    TaskSchema(name='task B', dependencies=['task D', 'task E']),
                    TaskSchema(name='task F', dependencies=['task B']),
                    # sub-tasks:
                    TaskSchema(name='task Q', dependencies=[]),
                    TaskSchema(name='task Y', dependencies=['task C']),
                    TaskSchema(name='task C', dependencies=[]),
                    TaskSchema(name='task D', dependencies=[]),
                    TaskSchema(name='task E', dependencies=['task Q']),
                ]
            ),
            ['task I', 'task A', 'task B', 'task F'],  # expected order
            id='[003] 2 tasks with equal resolved deps len',
        ),
        # [004] one task has more equal sub task then different - it goes first
        pytest.param(
            BuildSchema(name='test build', tasks=['task A', 'task B']),
            TasksSchema(
                tasks=[
                    # build tasks:
                    TaskSchema(name='task B', dependencies=['task Q', 'task Y']),
                    TaskSchema(name='task A', dependencies=['task D', 'task E']),
                    #
                    # sub-tasks:
                    # 3 uniq task
                    TaskSchema(name='task Q', dependencies=['task C']),  # the same task twice
                    TaskSchema(name='task Y', dependencies=['task C']),  # the same task twice
                    #
                    # 4 uniq task
                    TaskSchema(name='task D', dependencies=['task C']),
                    TaskSchema(name='task E', dependencies=['task Q']),
                    #
                    # sub-sub-tasks:
                    TaskSchema(name='task C', dependencies=[]),
                    TaskSchema(name='task Q', dependencies=[]),
                ]
            ),
            ['task B', 'task A'],  # expected order
            id='[004] one task has more equal sub task then different - it goes first',
        ),
    ],
)
def test_tasks_sorting(build: BuildSchema, tasks: TasksSchema, expected: list[str]):
    store = tasks.as_store()
    random.shuffle(build.tasks)  # NOTE: to be sure it will be sorted right independently of incoming tasks order

    assert expected == [task.name for task in build.resolve(store)]


# ['forward_interest', 'front_arm', 'reach_wind', 'voice_central', 'write_beautiful']
@pytest.mark.parametrize(
    ['build_name', 'expected'],
    [
        pytest.param(
            # build name:
            'forward_interest',
            [
                # expected order:
                'build_teal_leprechauns',
                'write_fuchsia_golems',
                'coloring_navy_golems',
                'enable_olive_humans',
                'enable_lime_leprechauns',
                'enable_lime_leprechauns',
                'enable_silver_humans',
                'coloring_aqua_centaurs',
                'write_blue_ogres',
            ],
            id='[001] forward_interest',
        ),
        pytest.param(
            # build name:
            'front_arm',
            [
                # expected order:
                'build_lime_golems',
                'design_maroon_witches',
                'read_aqua_orcs',
                'design_teal_golems',
                'train_white_leprechauns',
                'design_yellow_centaurs',
                'read_gray_golems',
                'upgrade_gray_humans',
                'coloring_black_goblins',
                'map_purple_humans',
            ],
            id='[002] front_arm',
        ),
        # TODO other builds
    ],
)
def test_tasks_sorting_from_yaml(build_name: str, expected: list[str]):
    builds_schema = BuildsSchema.parse_yaml(settings.BUILDS_FILE_PATH)
    tasks_schema = TasksSchema.parse_yaml(settings.TASKS_FILE_PATH)
    builds_store = builds_schema.as_store()
    tasks_store = tasks_schema.as_store()

    build = builds_store[build_name]
    random.shuffle(build.tasks)
    # pprint([task.name for task in build.resolve(tasks_store)])

    assert expected == [task.name for task in build.resolve(tasks_store)]

    # TODO separate test
    # Speed test:
    def _do_speed_test():
        for task in tasks_store.values():
            task.release_cash()
        build.resolve(tasks_store)

    taken_seconds = timeit('_do_speed_test()', globals=locals(), number=10000)
    logger.info(f'Speed test: {taken_seconds}. ')
