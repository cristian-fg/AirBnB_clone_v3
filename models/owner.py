#!/usr/bin/python
""" class owner"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Owner(BaseModel, Base):
    """Representation of owner """
    if models.storage_t == "db":
        __tablename__ = 'owners'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        pets = relationship("Pet", backref="owner")
    else:
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """init a owner"""
        super().__init__(*args, **kwargs)
