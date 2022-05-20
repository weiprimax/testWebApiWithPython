from collections import defaultdict
import os
import json
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
    print(f'hello:{API_KEY} {CERT_CONTOSO} {API_TODO_LOCAL}')
    # weather_info = retrieve_weather_with_adapter(city="London", adapter=fake_adapter)
    # weather_info = retrieve_weather_with_adapter(
    #    city="London", adapter=requests_adapter)
    # todo_item = retrieve_todo_with_adapter(
    #    api=API_TODO_REMOTE, adapter=requests_adapter)
    #todo_item = post_todo_with_adapter(api=API_TODO_LOCAL,
    #                       post_adapter=requests_adapter_post)

    pem_path = os.path.join(os.getcwd(), PEM_CONTOSO)
    print(pem_path)
    retrieve_todo_with_adapter(
        api=API_TODO_CONTOSO, adapter=requests_adapter, pem=pem_path)


def cube(n):
    return n*n*n


def requests_adapter(url: str, pem=False) -> dict:
    """An adapter that encapsulates requests.get"""
    #s = requests.Session()
    #s.cert = cert
    #resp = requests.get(url)
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


def find_todo_with_adapter_for(api: str, adapter: Callable[[str], dict], pem=False) -> dict:
    """Find the todo using an adapter."""
    # url = API.format(city_name=city, api_key=API_KEY)
    url = api
    return adapter(url, pem)


def retrieve_todo_with_adapter(
    api: str, adapter: Callable[[str], dict] = requests_adapter, pem=False
) -> TypeList[LiteDbTodoItem]:
    """Retrieve todo implementation that uses an adapter."""
    data = find_todo_with_adapter_for(api, adapter=adapter, pem=pem)
    data_len = len(data)
    items = []
    for i in range(data_len):
        items.append(LiteDbTodoItem.from_dict(data[i]))
        # print(f'id:{result[i].item_id}')
    return items

    # return LiteDbTodoItem.from_dict(data)


def requests_adapter_post(url: str, body, header, pem=False) -> dict:
    """An adapter that encapsulates requests.get"""
    resp = requests.post(url, data=json.dumps(body), headers=header, verify=pem)
    print(f'get status code:{resp.status_code}')
    resp.raise_for_status()
    return resp.json()


def init_normal_header(headers: dict) -> dict:
    headers['Content-Type'] = 'application/json'
    headers['Age'] = '20'
    headers['token'] = '20'
    headers['accept'] = 'text/plain'

def post_todo_with_adapter_for(api: str, post_adapter: Callable[[str, Any, Any], dict], pem=False) -> dict:
    """Find the todo using an adapter."""
    # url = API.format(city_name=city, api_key=API_KEY)
    url = api
    headers, body = {}, {}
    headers = {}
    init_normal_header(headers)
    print(f'init:{headers}')
    body['name'] = 'go'
    body['isComplete'] = True
    return post_adapter(url, body, headers, pem)


def post_todo_with_adapter(
    api: str, post_adapter: Callable[[str, Any, Any], dict] = requests_adapter, pem=False
) -> LiteDbTodoItem:
    """Retrieve todo implementation that uses an adapter."""
    data = post_todo_with_adapter_for(api, post_adapter=post_adapter, pem=pem)
    return LiteDbTodoItem.from_dict(data)


def format_date(timestamp: int) -> str:
    """Formats a timestamp into date time."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%m/%d/%Y, %H:%M:%S")


if __name__ == '__main__':
    main()
