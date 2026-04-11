from pydantic import BaseModel

class UserInput(BaseModel):
    risk: str
    duration_years: int
    budget: int