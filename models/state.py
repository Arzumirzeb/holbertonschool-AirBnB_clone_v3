#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base, BaseModel
from models.city import City
from os import getenv
import models


class State(BaseModel, Base):
    """State Model"""

    __tablename__ = "states"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    cities: Mapped[list["City"]] = relationship("City", backref="state",
                                                cascade="delete")
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all linked City objects."""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list