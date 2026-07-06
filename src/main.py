from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Body, FastAPI, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import engine, new_session
from src.database.models import Base
from src.exceptions import NoLongUrlProvidedError, SlugAlreadyExistsError
from src.service import generate_short_url, get_url_by_slug
from src.database.crud import increment_clicks, get_clicks_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


@app.get("/{short_id}")
async def redirect_to_url(
    short_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        long_url = await get_url_by_slug(short_id, session)
    except NoLongUrlProvidedError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Short URL not found.")
    await increment_clicks(short_id, session)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)

@app.post("/shorten")
async def shorten_url(    
    long_url: Annotated[str, Body(embed=True)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        new_slug = await generate_short_url(long_url, session)
    except SlugAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to generate a unique slug.")
    return {"data": new_slug}   


@app.get("/stats/{short_id}")
async def get_url_stats(
    short_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    clicks = await get_clicks_by_slug(short_id, session)

    if clicks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found.",
        )

    return {"short_id": short_id, "clicks": clicks}   
