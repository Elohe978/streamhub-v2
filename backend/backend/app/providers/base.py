from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass
class ProviderPlayback:
    provider_id: str
    url: str
    format: Literal["hls", "dash", "mp4"]
    expires_at: datetime | None = None
    authorized: bool = False

class StreamingProvider(ABC):
    provider_id: str

    @abstractmethod
    async def get_playback(self, content_id: str) -> ProviderPlayback | None:
        """Return a playback URL issued by a provider the operator is authorized to use."""
        raise NotImplementedError
