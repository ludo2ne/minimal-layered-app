from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from controller import player_controller
from utils.log_utils import get_logger, initialize_logs

logger = get_logger(__name__)

initialize_logs("Webservice")
app = FastAPI()
app.include_router(player_controller.router, prefix="/player", tags=["Players"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
