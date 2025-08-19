from typing import Annotated

from pydantic import BaseModel, Field


class Config(BaseModel):
    envious_max_len: int = 10
    envious_probability: Annotated[float, Field(ge=0.0, le=1.0)] = 0.7
    envious_list: list[str] = ["koishi", "华为"]
