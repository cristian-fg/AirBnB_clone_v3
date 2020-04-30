#!/usr/bin/python3
""" pet"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Pet(BaseModel, Base):
    """Representation pet """
    if models.storage_t == "db":
        __tablename__ = 'pets'
        owner_id = Column(String(60), ForeignKey('owners.id'), nullable=False)
        name = Column(String(128), nullable=False)
        age = Column(Integer, nullable=False, default=0)
        color = Column(String(128), nullable=False)
        owners = relationship("Owner", backref="owner")
    else:
        owner_id = ""
        name = ""
        age = 0
        color = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
