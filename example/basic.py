from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import APIRouter
from fastapi import Body
from fastapi import Form
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/bigger-applications/
router = APIRouter(prefix="/basic", tags=["basic"])


# Path value
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/{item_id}/{model_name}/{text}")
async def get_model(
    item_id: int, model_name: ModelName, text: str = Path(title="test text")
):
    return {
        "model_name": model_name,
        "item_id": item_id,
        "text": text,
    }


# Query params
@router.get("/with_q")
async def read_item(
    q: str | None = None,
    p: str
    | None = Query(
        default=...,
        max_length=50,
        description="Query string for the items to search in the database that have a good match",
        example="hello",
    ),
):
    return {"q": q, "p": p}


# Body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@router.post("/")
async def create_item(item: Item):
    return item


@router.put("/")
async def update_item(
    *,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item": item}
    return results


# Header
@router.get("/header")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


# Response


class ItemR(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@router.post("/create")
async def create_item(item: ItemR) -> ItemR:
    return item


@router.post("/another_create", response_model=ItemR)
async def create_item(item: ItemR) -> Any:
    return item


# Form
@router.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# Error handling


@router.get("/fail")
async def read_item():
    raise HTTPException(status_code=404, detail="Item not found")


# Meta data
@router.post(
    "/meta/",
    response_model=Item,
    tags=["tag1", "test2"],
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item


# JSON


class JsonItem(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@router.put("/json/")
def update_item(item: Item) -> dict:
    json_compatible_item_data = jsonable_encoder(item)
    return json_compatible_item_data
