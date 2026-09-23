class Player:
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"Player({self.username})"
