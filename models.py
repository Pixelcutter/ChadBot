from dataclasses import dataclass

@dataclass
class Emoji():
    id: int
    emoji: str
    sentiment_score: float
    name: str
    guild_id: int
    url: str

