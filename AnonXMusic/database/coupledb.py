from threading import RLock
from datetime import datetime
from AnonXMusic.database import MongoDB

INSERTION_LOCK = RLock()

class CouplesDB(MongoDB):
    """Class for managing Couples in the bot."""

    db_name = "couples"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def get_couple(self, chat_id: int, date: str):
        with INSERTION_LOCK:
            return self.find_one({"chat_id": chat_id, "date": date})

    def save_couple(self, chat_id: int, date: str, couple: dict):
        with INSERTION_LOCK:
            couple_data = {
                "chat_id": chat_id,
                "date": date,
                "c1_id": couple["c1_id"],
                "c2_id": couple["c2_id"],
            }
            return self.insert_one(couple_data)

    def update_couple(self, chat_id: int, date: str, update: dict):
        with INSERTION_LOCK:
            return self.update({"chat_id": chat_id, "date": date}, update)

    def find_all_couples(self):
        with INSERTION_LOCK:
            return self.find_all()

    def load_from_db(self):
        with INSERTION_LOCK:
            return self.find_all()
