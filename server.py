from fastapi import FastAPI, Request
from pydantic import BaseModel
from time import sleep
import threading
import requests


class Item(BaseModel):
    my_port: str


app = FastAPI()

thread = None


def thread_function(url, data, sleep_time):
    sleep(sleep_time)
    response = requests.post(url, json=data)
    print(response.text)


@app.post("/ping")
async def pong(item: Item):
    global thread
    my_port = "8001" if (item.my_port == "0" or item.my_port == "8000") else "8000"
    other_port = "8000" if my_port == "8001" else "8001"
    print("my_port", my_port, "other_port", other_port)
    sleep(1)
    url = f'http://127.0.0.1:{other_port}/ping'
    data = {'my_port': f'{my_port}'}
    thread = threading.Thread(target=thread_function, args=(url, data, 1))
    thread.start()
    return {"ping": "pong"}