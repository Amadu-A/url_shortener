from src.service import generate_short_url, get_url_by_slug


async def test_generate_short_url(session):
    res = await generate_short_url("https://www.example.com", session=session)
    assert isinstance(res, str)
    assert len(res) == 6
    