from fastapi import APIRouter, Depends, HTTPException

from service.player_service import PlayerService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_player_service():
    """Dependency Injection provider for PlayerService."""
    return PlayerService()


@router.get("/hello/{username}")
def say_hello(username: str, player_service=Depends(get_player_service)):
    logger.info("Say Hello")
    message = player_service.get_greeting(username)
    if message:
        return {"message": message}
    raise HTTPException(status_code=404, detail="Unknown user")
