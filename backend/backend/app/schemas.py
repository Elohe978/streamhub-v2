from datetime import datetime, timedelta, timezone
from typing import Literal
from pydantic import BaseModel, HttpUrl, Field

MediaType = Literal["movie", "series"]
StreamFormat = Literal["hls", "dash", "mp4"]

class ContentItem(BaseModel):
    id: str
    title: str
    year: int
    media_type: MediaType = "movie"
    overview: str = ""
    poster_url: str | None = None
    backdrop_url: str | None = None
    genres: list[str] = Field(default_factory=list)

class PlaybackRequest(BaseModel):
    content_id: str
    provider_id: str = "configured-provider"

class PlaybackSource(BaseModel):
    provider_id: str
    format: StreamFormat
    url: HttpUrl
    expires_at: datetime | None = None

class PlaybackSession(BaseModel):
    session_id: str
    status: Literal["ready", "unavailable"]
    content_id: str
    source: PlaybackSource | None = None
    message: str | None = None
