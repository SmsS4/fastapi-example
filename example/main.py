import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse


def main() -> None:
    app = FastAPI()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
