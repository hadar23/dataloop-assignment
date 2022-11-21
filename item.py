from pydantic import BaseModel


class Item(BaseModel):
    my_port: str
    command: str
