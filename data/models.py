from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from data.database import db


class WbAccount(db.Model):
    __tablename__ = "wb_accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(100))
    api_key: Mapped[str] = mapped_column(String(511), unique=True)
    is_active: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default="CURRENT_TIMESTAMP")
    last_sync: Mapped[Optional[datetime]] = mapped_column()

    def __repr__(self) -> str:
        return f"WBAccount(id={self.id!r}, account_name={self.name!r}, is_active={self.is_active!r})"


class WbCard(db.Model):
    __tablename__ = "wb_cards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    photos: Mapped[List["WbPhotos"]] = relationship(back_populates="card")


class WbPhotos(db.Model):
    __tablename__ = "wb_photos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    big: Mapped[str] = mapped_column(String(1000))
    c246x328: Mapped[str] = mapped_column(String(1000))
    c516x688: Mapped[str] = mapped_column(String(1000))
    square: Mapped[str] = mapped_column(String(1000))
    tm: Mapped[str] = mapped_column(String(1000))

    card_id: Mapped[int] = mapped_column(ForeignKey("wb_cards.id"))
    card: Mapped["WbCard"] = relationship(back_populates="photos")
