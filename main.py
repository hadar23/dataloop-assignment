from fastapi import FastAPI
from pydantic import BaseModel
import requests


class Item(BaseModel):
    my_port: str


app = FastAPI()

firs_url = 'http://127.0.0.1:8000/ping'

first_data = {'my_port': '0'}


def first_ping():
    response = requests.post(firs_url, json=first_data)
    print(response.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    first_ping()