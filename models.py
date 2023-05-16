from dataclasses import dataclass

@dataclass
class Emoji():
    id: int
    emoji: str
    sentiment_score: float = 0
    name: str = "generic"
    guild_id: int = 0
    url: str = None

@dataclass
class User():
    id: int
    name: str
    display_avatar: str
    msg_count: int = 0
    toxic_msg_count: int = 0
    toxicity_score: int = 0

@dataclass
class Message():
    id: int
    author_id: str
    channel_id: int
    guild_id: int
    text: str
    created_at: str
    jump_url: str
    is_toxic: int = 0

