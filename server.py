from utils.item import Item
from fastapi import FastAPI
from time import sleep
import threading
import requests


class PingPongThread(threading.Thread):
    def __init__(self, my_port, other_port):
        threading.Thread.__init__(self)
        self.my_port = my_port
        self.other_port = other_port
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.command = ''

    def run(self):
        global thread_8000_pause, thread_8001_pause, sleep_time
        while True:
            while (self.my_port == "8000" and thread_8000_pause) or (self.my_port == "8001" and thread_8001_pause):
                print(self.my_port, "paused")
                sleep(sleep_time)
            url = f'http://127.0.0.1:{self.other_port}/ping'
            data = {'my_port': f'{self.my_port}', 'command': self.command}
            self.command = ""
            sleep(sleep_time)
            response = requests.post(url, json=data)
            print(response.text)


app = FastAPI()

thread_8000 = None
thread_8001 = None

thread_8000_pause = False
thread_8001_pause = False
sleep_time = 1

@app.post("/ping")
async def pong(item: Item):
    global thread_8000, thread_8001, thread_8000_pause, thread_8001_pause
    my_port = "8000" if (item.my_port == "0" or item.my_port == "8001") else "8001"
    other_port = "8000" if my_port == "8001" else "8001"
    command = item.command

    if my_port == "8000":
        if thread_8000 is None:
            thread_8000 = PingPongThread(my_port, other_port)
        if command == "start":
            print("in start 8000")
            thread_8000.command = command
            thread_8000.start()
        if command == "pause":
            print("in pause 8000")
            thread_8000.command = command
            sleep(sleep_time*2)
            thread_8000_pause = True
        if command == "resume":
            print("in pause 8000")
            thread_8000.command = command
            thread_8000_pause = False

    if my_port == "8001":
        if thread_8001 is None:
            thread_8001 = PingPongThread(my_port, other_port)
        if command == "start":
            print("in start 8001")
            thread_8001.start()
        if command == "pause":
            print("in pause 8001")
            thread_8001_pause = True
        if command == "resume":
            print("in resume 8001")
            thread_8001_pause = False

    return {"ping": "pong"}