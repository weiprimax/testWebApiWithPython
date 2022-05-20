from testWebApi import *
from api_lib import *
import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


def test_cube():
    assert cube(2) == 8
    #assertEquals(cube(2), 8)


@pytest.mark.weather
def test_weather():
    weather_info = retrieve_weather_with_adapter(
        city="London", adapter=requests_adapter)
    assert weather_info.temp > 0


@pytest.mark.local
def test_todo_local():
    todo_items = retrieve_todo_with_adapter(
        api=API_TODO_LOCAL, adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.local
def test_todo_post_local():
    todo_item = post_todo_with_adapter(api=API_TODO_LOCAL,
                                       post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


@pytest.mark.contoso
def test_todo_contoso():
    todo_items = retrieve_todo_with_adapter(
        api=API_TODO_CONTOSO,
        adapter=requests_adapter,
        pem=PEM_CONTOSO)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.contoso
def test_todo_post_contoso():
    todo_item = post_todo_with_adapter(
        api=API_TODO_LOCAL,
        post_adapter=requests_adapter_post,
        pem=PEM_CONTOSO)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


@pytest.mark.skip(reason="no way of currently testing this")
def test_todo_remote():
    todo_items = retrieve_todo_with_adapter(
        api=API_TODO_REMOTE,
        adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.skip(reason="no way of currently testing this")
def test_todo_post_remote():
    todo_item = post_todo_with_adapter(api=API_TODO_REMOTE,
                                       post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1
