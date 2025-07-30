from pydantic import BaseModel, constr
from typing import List


class PlanDTO(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
