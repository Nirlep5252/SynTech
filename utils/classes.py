class Item:
    def __init__(self, prize: int, name: str, description: str, emoji: str) -> None:
        self.prize: int = prize
        self.name: str = name
        self.description: str = description
        self.emoji: str = emoji
