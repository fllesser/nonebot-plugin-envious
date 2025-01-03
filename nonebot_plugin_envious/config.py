from pydantic import BaseModel
from pathlib import Path

class Config(BaseModel):
    ENVIOUS_MAX_LEN: int = 10
    ENVIOUS_LIST: list[str] = ['koishi']
