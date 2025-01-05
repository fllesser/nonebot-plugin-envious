from pydantic import BaseModel, confloat

class Config(BaseModel):
    envious_max_len: int = 10
    envious_probability: confloat(ge=0.0, le=1.0) = 0.7
    envious_list: list[str] = ['koishi']
    