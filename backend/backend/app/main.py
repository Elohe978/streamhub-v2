from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .catalog import list_content, get_content
from .schemas import ContentItem, PlaybackRequest, PlaybackSession, PlaybackSource
from .providers.configured_provider import ConfiguredProvider

app = FastAPI(title=settings.app_name, version="0.1.0")

# Restrict origins before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else [],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "streamhub-api"}

@app.get(f"{settings.api_prefix}/home")
async def home():
    items = list_content()
    return {"featured": items[:1], "popular": items, "continue_watching": []}

@app.get(f"{settings.api_prefix}/search")
async def search(q: str = Query(default="", max_length=120)):
    results = list_content(q or None)
    return {"results": results, "total": len(results)}

@app.get(f"{settings.api_prefix}/content", response_model=list[ContentItem])
async def content_list():
    return list_content()

@app.get(f"{settings.api_prefix}/content/{content_id}", response_model=ContentItem)
async def content_details(content_id: str):
    item = get_content(content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")
    return item

@app.post(f"{settings.api_prefix}/playback/sessions", response_model=PlaybackSession)
async def create_playback_session(request: PlaybackRequest):
    item = get_content(request.content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")

    provider = ConfiguredProvider()
    playback = await provider.get_playback(request.content_id)

    if not playback or not playback.authorized:
        return PlaybackSession(
            session_id=str(uuid4()),
            status="unavailable",
            content_id=request.content_id,
            message="No authorized playback source is configured for this content.",
        )

    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    return PlaybackSession(
        session_id=str(uuid4()),
        status="ready",
        content_id=request.content_id,
        source=PlaybackSource(
            provider_id=playback.provider_id,
            format=playback.format,
            url=playback.url,
            expires_at=expires,
        ),
    )
