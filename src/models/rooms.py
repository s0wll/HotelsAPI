from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base



class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]  # Кол-во таких номеров в отеле

    facilities: Mapped[list["FacilitiesOrm"]] = relationship( # type: ignore
        back_populates="rooms",
        secondary="rooms_facilities",
    )