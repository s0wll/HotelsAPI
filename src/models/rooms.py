import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base
if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]  # Кол-во таких номеров в отеле

    facilities: Mapped[list["FacilitiesOrm"]] = relationship( # Relationship аттрибут для получения данных из взаимосвязанных таблиц
        back_populates="rooms",
        secondary="rooms_facilities",
    )