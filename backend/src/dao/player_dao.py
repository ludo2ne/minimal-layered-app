import sqlite3

from business_object.player import Player
from utils.log_utils import get_logger, log

logger = get_logger(__name__)


class PlayerDAO:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS player")
            conn.execute("CREATE TABLE player (username TEXT PRIMARY KEY)")
            conn.execute("INSERT INTO player VALUES ('alice')")

    @log
    def get_player_by_username(self, username: str) -> Player:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT username
                     FROM player
                    WHERE UPPER(username) = UPPER(?)
                """,
                (username,),
            )
            row = cursor.fetchone()
            if row:
                return Player(username=row[0])
            return None
