from fastapi import FastAPI

from app.modules.a_ping import ping


def create_application() -> FastAPI:
    app = FastAPI(title='JoelCelAPI')
    app.include_router(ping.router)

    return app


app = create_application()
