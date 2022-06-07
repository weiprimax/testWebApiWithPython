from testWebApi import *
from api_lib import *
import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


def test_cube():
    assert cube(2) == 8


@pytest.mark.skip(reason="do not test weather")
@pytest.mark.weather
def test_weather():
    weather_info = retrieve_weather_with_adapter(
        city="London",
        adapter=requests_adapter)
    assert weather_info.temp > 0


@pytest.mark.local
def test_todo_local():
    todo_items = retrieve_todos_with_adapter(
        api=API_TODO_LOCAL,
        adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.local
def test_todo_post_local():
    todo_item = post_todo_with_adapter(
        api=API_TODO_LOCAL,
        post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


@pytest.mark.local
def test_device_post_local():
    device_respond = post_device_with_adapter(
        api=API_DEVICE_LOCAL,
        post_adapter=requests_adapter_post, fw_version=FW_VERSION_OLD)
    print(f'resp:{device_respond}')
    assert device_respond.Code == 2000
    assert FW_VERSION_NEW in device_respond.fwdata.new_version
    assert "http" in device_respond.fwdata.fw_link
    device_respond = post_device_with_adapter(
        api=API_DEVICE_LOCAL,
        post_adapter=requests_adapter_post, fw_version=FW_VERSION_NEW)
    print(f'resp:{device_respond}')
    assert device_respond.Code == 2000
    assert FW_VERSION_NEW2 in device_respond.fwdata.new_version
    assert "http" in device_respond.fwdata.fw_link


@pytest.mark.local
def test_device_post_local_wrong():
    device_respond = post_device_with_adapter(
        api=API_DEVICE_LOCAL,
        post_adapter=requests_adapter_post,
        use_right_head=False)
    print(f'resp:{device_respond}')
    assert device_respond.Code == 4000


@pytest.mark.local
def test_device_local():
    device_items = retrieve_devices_with_adapter(
        api=API_DEVICE_LOCAL,
        adapter=requests_adapter)
    for item in device_items:
        assert item.Id >= 1


@pytest.mark.contoso
def test_todo_contoso():
    todo_items = retrieve_todos_with_adapter(
        api=API_TODO_CONTOSO,
        adapter=requests_adapter,
        pem=PEM_CONTOSO)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.contoso
def test_todo_post_contoso():
    todo_item = post_todo_with_adapter(
        api=API_TODO_CONTOSO,
        post_adapter=requests_adapter_post,
        pem=PEM_CONTOSO)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


# @pytest.mark.skip(reason="only test in primax")
@pytest.mark.remote
def test_todo_remote():
    todo_items = retrieve_todos_with_adapter(
        api=API_TODO_REMOTE,
        adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


# @pytest.mark.skip(reason="only test in primax")
@pytest.mark.remote
def test_todo_post_remote():
    todo_item = post_todo_with_adapter(
        api=API_TODO_REMOTE,
        post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


@pytest.mark.remote
def test_device_post_remote():
    device_respond = post_device_with_adapter(
        api=API_DEVICE_REMOTE,
        post_adapter=requests_adapter_post)
    print(f'{device_respond}')
    assert device_respond.Res_code == 1


@pytest.mark.remote
def test_device_remote():
    device_items = retrieve_devices_with_adapter(
        api=API_DEVICE_REMOTE,
        adapter=requests_adapter)
    for item in device_items:
        assert item.Id >= 1


@pytest.mark.primax
def test_todo_primax():
    todo_items = retrieve_todos_with_adapter(
        api=API_TODO_PRIMAX,
        adapter=requests_adapter)
    for item in todo_items:
        assert item.item_id >= 1


@pytest.mark.primax
def test_todo_post_primax():
    todo_item = post_todo_with_adapter(
        api=API_TODO_PRIMAX,
        post_adapter=requests_adapter_post)
    print(f'{todo_item}')
    assert todo_item.item_id >= 1


@pytest.mark.primax
def test_device_post_primax():
    device_respond = post_device_with_adapter(
        api=API_DEVICE_PRIMAX,
        post_adapter=requests_adapter_post)
    print(f'{device_respond}')
    assert device_respond.Res_code == 1


@pytest.mark.primax
def test_device_primax():
    device_items = retrieve_devices_with_adapter(
        api=API_DEVICE_PRIMAX,
        adapter=requests_adapter)
    for item in device_items:
        assert item.Id >= 1
