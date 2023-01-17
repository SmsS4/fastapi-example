from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


router = APIRouter(
    dependencies=[Depends(verify_key)],
)


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    yield {"q": q, "skip": skip, "limit": limit}
    print("execute after response")


@router.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@router.get("/items2/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@router.get("/items3/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
