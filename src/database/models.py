from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class ShortURL(Base):
    __tablename__ = "short_urls"

    slug: Mapped[str] = mapped_column(String, primary_key=True)
    long_url: Mapped[str]
    clicks: Mapped[int] = mapped_column(default=0)
    