from testWebApi import *
from api_lib import *


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


def test_cube():
    assert cube(2) == 8
    #assertEquals(cube(2), 8)


def test_weather():
    weather_info = retrieve_weather_with_adapter(
        city="London", adapter=requests_adapter)
    assert weather_info.temp > 0


def test_weather2():
    weather_info2 = retrieve_weather_with_adapter(
        city="London", adapter=urllib_adapter)
    assert weather_info2.temp > 0


def test_todo_remote():
    todo_items = retrieve_todo_with_adapter(
        api=API_TODO_REMOTE, adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


def test_todo_local():
    todo_items = retrieve_todo_with_adapter(
        api=API_TODO_LOCAL, adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


def test_todo_post_local():
    todo_item = post_todo_with_adapter(api=API_TODO_LOCAL,
                                       post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


def test_todo_post_remote():
    todo_item = post_todo_with_adapter(api=API_TODO_REMOTE,
                                       post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1
