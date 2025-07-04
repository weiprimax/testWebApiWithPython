from collections import defaultdict
from ctypes.wintypes import LONG
import dataclasses
import os
import json
from pickle import FALSE, TRUE
from sre_constants import IN
import time
import calendar
import hashlib
import urllib.request
import requests
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, AnyStr, Callable, List as TypeList
from api_lib import *


# API_KEY = os.environ["api_key"]
API_KEY = "a52f97f5da4ba6672b101d6780af590a"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API = BASE_URL + "?q={city_name}&appid={api_key}&units=metric"
DEVICE_NAME = "00007928-6216-4353-a38a-78d2ca9ce47f"
PRODUCT_CODE = "A83A9"
FW_VERSION_OLD = "V0.0.0"
FW_VERSION_NEW = "V99.9.9"
FW_VERSION_NEW2 = "V3.0.1"
FW_VERSION_090 = "V0.9.0"


@dataclass
class LiteDbDeviceItem:
    Id: int
    Device_id: str
    Product_code: str

    @classmethod
    def from_dict(cls, data: dict) -> "LiteDbDeviceItem":
        return cls(
            Id=data["id"],
            Device_id=data["device_id"],
            Product_code=data["product_Code"]
        )


@dataclass
class LiteDbDeviceItemRespondFwData:
    new_version: str
    fw_link: str

    def from_dict(cls, data: dict) -> "LiteDbDeviceItemRespondFwData":
        return cls(
            new_version=data['new_version'],
            fw_link=data['fw_link']
        )


@dataclass
class LiteDbDeviceItemRespond:
    Code: str
    Message: str
    fwdata: LiteDbDeviceItemRespondFwData

    @classmethod
    def from_dict(cls, data: dict) -> "LiteDbDeviceItemRespond":
        input_data = LiteDbDeviceItemRespondFwData.from_dict(
            cls=LiteDbDeviceItemRespondFwData, data=data["data"]) if data["data"] else None
        return cls(
            Code=data["code"],
            Message=data["msg"],
            fwdata=input_data
        )


@dataclass
class LiteDbTodoItem:
    item_id: int
    item_name: str
    item_is_complete: bool

    @classmethod
    def from_dict(cls, data: dict) -> "LiteDbTodoItem":
        return cls(
            item_id=data["id"],
            item_name=data["name"],
            item_is_complete=data["isComplete"]
        )

    # @classmethod
    # def to_dict(cls) -> typing.Dict:
    # dict = {"id": cls.item_id "name": cls.item_name, "isComplete": cls.item_is_complete}


@dataclass
class WeatherInfo:
    """Stores weather information."""

    temp: float
    sunset: str
    sunrise: str
    temp_min: float
    temp_max: float
    desc: str

    @classmethod
    def from_dict(cls, data: dict) -> "WeatherInfo":
        return cls(
            temp=data["main"]["temp"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            desc=data["weather"][0]["main"],
            sunset=format_date(data["sys"]["sunset"]),
            sunrise=format_date(data["sys"]["sunrise"]),
        )


def main():
    print(f'hello: {CERT_CONTOSO} {API_TODO_LOCAL}')
    pem_path = os.path.join(os.getcwd(), PEM_CONTOSO)
    print(pem_path)
    #retrieve_todos_with_adapter(
    #    api=API_TODO_CONTOSO, adapter=requests_adapter, pem=pem_path)
    device_respond = post_device_with_adapter(
        API_VERSION_CHECK_ANKER,
        post_adapter=requests_adapter_post, fw_version=FW_VERSION_090, pem=PEM_ANKER)
    print(f'resp:{device_respond}')


def cube(n):
    return n*n*n


def requests_adapter(url: str, pem=False) -> dict:
    """An adapter that encapsulates requests.get"""
    resp = requests.get(url, verify=pem)
    print(f'get status code:{resp.status_code}')

    return resp.json()


def urllib_adapter(url: str) -> dict:
    """An adapter that encapsulates urllib.urlopen"""
    with urllib.request.urlopen(url) as response:
        resp = response.read()
    return json.loads(resp)


def find_weather_with_adapter_for(city: str, adapter: Callable[[str], dict]) -> dict:
    """Find the weather using an adapter."""
    url = API.format(city_name=city, api_key=API_KEY)
    return adapter(url)


def retrieve_weather_with_adapter(
    city: str, adapter: Callable[[str], dict] = requests_adapter
) -> WeatherInfo:
    """Retrieve weather implementation that uses an adapter."""
    data = find_weather_with_adapter_for(city, adapter=adapter)
    return WeatherInfo.from_dict(data)


def retrieve_todo_with_adapter_inner(api: str, adapter: Callable[[str], dict], pem=False) -> dict:
    """Find the todo using an adapter."""
    # url = API.format(city_name=city, api_key=API_KEY)
    url = api
    return adapter(url, pem)


def retrieve_todos_with_adapter(
    api: str, adapter: Callable[[str], dict] = requests_adapter, pem=False
) -> TypeList[LiteDbTodoItem]:
    """Retrieve todo implementation that uses an adapter."""
    data = retrieve_todo_with_adapter_inner(api, adapter=adapter, pem=pem)
    data_len = len(data)
    items = []
    for i in range(data_len):
        items.append(LiteDbTodoItem.from_dict(data[i]))
        # print(f'id:{result[i].item_id}')
    return items


def requests_adapter_post(url: str, body, header, pem=False) -> dict:
    """An adapter that encapsulates requests.get"""
    resp = requests.post(url, data=json.dumps(body),
                         headers=header, verify=pem)
    print(f'get status code:{resp.status_code}')
    # resp.raise_for_status()
    return resp.json()


def init_normal_header(headers: dict):
    headers['Content-Type'] = 'application/json'
    headers['Age'] = '20'
    headers['token'] = '20'
    headers['accept'] = 'text/plain'


def init_todo_body(body: dict):
    body['name'] = 'go'
    body['isComplete'] = True


def init_device_header(headers: dict):
    time_stamp = str(calendar.timegm(time.gmtime()))
    device_id = DEVICE_NAME
    str_md5_input = device_id + time_stamp
    result = hashlib.md5(str_md5_input.encode())
    token = result.hexdigest()
    headers['Content-Type'] = 'application/json'
    headers['Age'] = '20'
    headers['token'] = token
    headers['accept'] = 'application/json'
    headers['timestamp'] = time_stamp


def init_device_header_wrong(headers: dict):
    time_stamp = str(calendar.timegm(time.gmtime()))
    str_md5_input = time_stamp
    result = hashlib.md5(str_md5_input.encode())
    token = result.hexdigest()
    headers['Content-Type'] = 'application/json'
    headers['Age'] = '20'
    headers['token'] = token
    headers['accept'] = 'text/plain'
    headers['timestamp'] = time_stamp


def init_device_body(body: dict, fw_version: str):
    body['device_id'] = DEVICE_NAME
    body['product_code'] = PRODUCT_CODE
    body['fw_version'] = fw_version


def post_todo_with_adapter_inner(api: str, post_adapter: Callable[[str, Any, Any], dict], pem=False) -> dict:
    """Find the todo using an adapter."""
    # url = API.format(city_name=city, api_key=API_KEY)
    url = api
    headers, body = {}, {}
    init_normal_header(headers)
    print(f'init:{headers}')
    init_todo_body(body)
    print(f'init:{body}')
    return post_adapter(url, body, headers, pem)


def post_todo_with_adapter(
    api: str, post_adapter: Callable[[str, Any, Any], dict] = requests_adapter, pem=False
) -> LiteDbTodoItem:
    """Retrieve todo implementation that uses an adapter."""
    data = post_todo_with_adapter_inner(
        api, post_adapter=post_adapter, pem=pem)
    return LiteDbTodoItem.from_dict(data)


def retrieve_devices_with_adapter(
    api: str, adapter: Callable[[str], dict] = requests_adapter, pem=False
) -> TypeList[LiteDbDeviceItem]:
    data = retrieve_todo_with_adapter_inner(api, adapter=adapter, pem=pem)
    data_len = len(data)
    items = []
    for i in range(data_len):
        items.append(LiteDbDeviceItem.from_dict(data[i]))
        # print(f'id:{result[i].item_id}')
    return items


def post_device_with_adapter_inner(api: str, post_adapter: Callable[[str, Any, Any], dict], pem=False, use_right_head=True, fw_version="") -> dict:
    url = api
    headers, body = {}, {}
    if use_right_head:
        init_device_header(headers)
    else:
        init_device_header_wrong(headers)

    print(f'init:{headers}')
    init_device_body(body, fw_version)
    print(f'init:{body}')
    return post_adapter(url, body, headers, pem)


def post_device_with_adapter(
    api: str, post_adapter: Callable[[str, Any, Any], dict] = requests_adapter, pem=False, use_right_head=True, fw_version=""
) -> LiteDbDeviceItemRespond:
    """Retrieve respond after post deviceItem."""
    data = post_device_with_adapter_inner(
        api,
        post_adapter=post_adapter,
        pem=pem,
        use_right_head=use_right_head,
        fw_version=fw_version)
    print(f'resp data:{data}')
    return LiteDbDeviceItemRespond.from_dict(data)


def format_date(timestamp: int) -> str:
    """Formats a timestamp into date time."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%m/%d/%Y, %H:%M:%S")


if __name__ == '__main__':
    main()
