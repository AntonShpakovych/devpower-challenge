from typing import Annotated

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship

from config import DB_URL


engine = create_engine(DB_URL)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True, index=True)

    countries: Mapped[list["Country"]] = relationship(
        "Country",
        back_populates="region"
    )


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True, index=True)
    population: Mapped[int | None]

    region_id: Mapped[int] = mapped_column(
        ForeignKey(
            "regions.id",
            ondelete="CASCADE"
        )
    )
    region: Mapped["Region"] = relationship(
        "Region",
        back_populates="countries"
    )
