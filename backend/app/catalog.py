from .schemas import ContentItem

CATALOG = [
    ContentItem(
        id="sample-001",
        title="Sample Adventure",
        year=2024,
        media_type="movie",
        overview="Sample catalogue entry used to demonstrate discovery and details. "
                 "Replace this with metadata from a licensed catalogue provider.",
        genres=["Adventure", "Drama"],
    ),
    ContentItem(
        id="sample-002",
        title="The Science Files",
        year=2023,
        media_type="series",
        overview="A sample series record for testing the catalogue interface.",
        genres=["Documentary", "Science"],
    ),
]

def list_content(query: str | None = None) -> list[ContentItem]:
    if not query:
        return CATALOG
    q = query.casefold()
    return [item for item in CATALOG if q in item.title.casefold()
            or any(q in genre.casefold() for genre in item.genres)]

def get_content(content_id: str) -> ContentItem | None:
    return next((item for item in CATALOG if item.id == content_id), None)
