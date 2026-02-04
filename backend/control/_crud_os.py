# appending Crud() object with more specific functionality for model : os
from fastapi import APIRouter, \
                    HTTPException
from pydantic import BaseModel
from sqlmodel import select

from ._crud import Crud

class CrudOs(Crud):
    def __init__(self, model, 
                       name=''):
        Crud.__init__(self, 
                      model,
                      name)
        self.router = Crud.get_router(self)

    def get_router(self):
        router = self.router

        return router