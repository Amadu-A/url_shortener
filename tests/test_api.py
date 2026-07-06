import asyncio

from httpx import AsyncClient
import pytest

from src.database.crud import add_slug_to_db
from src.exceptions import SlugAlreadyExistsError


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/shorten", json={"long_url": "https://www.example.com"})
    assert result.status_code == 200


async def test_same_slug_from_two_sessions_raises_slug_already_exists(session_factory):
    """Тестируем запись существующего слага"""
    slug = "sLuG11"

    async with session_factory() as session_1, session_factory() as session_2:
        results = await asyncio.gather(
            add_slug_to_db(slug, "https://www.example.com/first", session_1),
            add_slug_to_db(slug, "https://www.example.com/second", session_2),
            return_exceptions=True,
        )

    assert sum(result is None for result in results) == 1
    assert sum(isinstance(result, SlugAlreadyExistsError) for result in results) == 1


async def test_concurrent_redirects_increment_clicks(ac: AsyncClient, session):
    """Тестируем увеличение счетчика при одновременном подключении и переходе по одной и той же ссылке"""
    slug = "sLuG11"
    await add_slug_to_db(slug, "https://www.example.com", session)

    first_response, second_response = await asyncio.gather(
        ac.get(f"/{slug}"),
        ac.get(f"/{slug}"),
    )

    assert first_response.status_code == 302
    assert second_response.status_code == 302

    stats_response = await ac.get(f"/stats/{slug}")

    assert stats_response.status_code == 200
    assert stats_response.json() == {"short_id": slug, "clicks": 2}
