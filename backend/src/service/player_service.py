from dao.player_dao import PlayerDAO
from utils.log_utils import get_logger, log

logger = get_logger(__name__)


class PlayerService:
    def __init__(self):
        self.dao = PlayerDAO()

    @log
    def get_greeting(self, username: str) -> str:
        player = self.dao.get_player_by_username(username)
        if player:
            return f"Hello {player.username}"
        return None
