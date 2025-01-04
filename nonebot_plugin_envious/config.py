from pydantic import BaseModel
from typing import Literal

PROBABILITY = Literal[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

class Config(BaseModel):
    ENVIOUS_MAX_LEN: int = 10
    ENVIOUS_PROBABILITY: PROBABILITY = 0.7
    ENVIOUS_LIST: list[str] = ['koishi']
    