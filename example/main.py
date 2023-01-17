import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

import time
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

def main() -> None:
    app = FastAPI(
        title="ChimichangApp",
        description='description',
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Deadpoolio the Amazing",
            "url": "http://x-force.example.com/contact/",
            "email": "dp@x-force.example.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        openapi_tags=tags_metadata,
        openapi_url="/api/v1/openapi.json",
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
