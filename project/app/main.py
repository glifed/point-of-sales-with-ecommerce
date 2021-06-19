from fastapi import FastAPI
import uvicorn

from modules.a_ping import ping


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(ping.router)

    return app


app = create_application()


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
