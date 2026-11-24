from .base import StreamingProvider, ProviderPlayback
from ..config import settings

class ConfiguredProvider(StreamingProvider):
    provider_id = "configured-provider"

    async def get_playback(self, content_id: str) -> ProviderPlayback | None:
        # Configure a test or licensed HLS URL in DEMO_HLS_URL.
        # A production adapter should call the provider's documented API,
        # validate the content entitlement, and return its authorized session URL.
        if not settings.demo_hls_url:
            return None
        return ProviderPlayback(
            provider_id=self.provider_id,
            url=settings.demo_hls_url,
            format="hls",
            authorized=True,
        )
