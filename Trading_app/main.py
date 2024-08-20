from datetime import datetime
from enum import Enum
from typing import List, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Trading App",
)

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "Shaman"},
    {"id": 3, "role": "trader", "name": "Mike"},
    {"id": 4, "role": "investor", "name": "Sam", "degree": [
        {"id":1}, {"created_at":"2020-01-01T00:00:00"}, {"type_degree": "expert"} ]},
]

fake_trades = [
    {"id": 1, "user_id": 2, "currency": "BTC", "side": "buy", "price": 5670, "amount": 2.12, },
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12, },
]

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: Optional[List[DegreeType]] = []

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: List[Degree]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str = Field(max_length=5)
    price: float = Field(ge=0)
    amount: float


@app.get("/users/{user_id}", response_model=List[User])
def get_users(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


def main() -> None:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()