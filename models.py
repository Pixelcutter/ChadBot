from dataclasses import dataclass
import asyncio
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
    toxic_flags_count: int = 0
    toxicity_score: int = 0

@dataclass
class ToxicReport():
    toxicity: int = 0
    severe_toxicity: int = 0
    threat: int = 0
    insult: int = 0
    identity_hate: int = 0
    # Make ToxicReport class able to be asynchronous
    def __await__(self):
        return self._async_generator().__await__()

    # What actually happens when await is called
    # Waits for 1 second 
    async def _async_generator(self):
        await asyncio.sleep(1)  
        return self

@dataclass
class Message():
    id: int
    author_id: int
    channel_id: int
    guild_id: int
    text: str
    created_at: str
    jump_url: str
    reactions: str = ""
    toxicity: int = 0
    severe_toxicity: int = 0
    threat: int = 0
    insult: int = 0
    identity_hate: int = 0
    was_analyzed: int = 0

