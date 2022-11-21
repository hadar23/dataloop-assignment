from fastapi import FastAPI
import requests
import sys


app = FastAPI()

firs_url = 'http://127.0.0.1:8000/ping'


def send_command_to_server(command):
    data = {'my_port': '0', 'command': f'{command}'}
    response = requests.post(firs_url, json=data)
    print(response.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    command = sys.argv[1]
    print(command)
    send_command_to_server(command)