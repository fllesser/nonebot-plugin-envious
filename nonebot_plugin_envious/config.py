from pydantic import BaseModel, confloat
from typing import Literal

class Config(BaseModel):
    ENVIOUS_MAX_LEN: int = 10
    ENVIOUS_PROBABILITY: confloat(ge=0.0, le=1.0) = 0.7
    ENVIOUS_LIST: list[str] = ['koishi']
    