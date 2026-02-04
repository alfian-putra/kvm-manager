# appending Crud() object with more specific functionality for model : vm
from fastapi import APIRouter, \
                    HTTPException
from pydantic import BaseModel
from sqlmodel import select

from ._crud import Crud


class CrudVm(Crud):
    def __init__(self, model, 
                       name=''):
        Crud.__init__(self, 
                      model,
                      name)
        self.router = Crud.get_router(self)

    def get_router(self):
        router = self.router

        # GET /vm?hostname='vm1'
        @router.get(f'/{self.name}?'+'hostname={hostname}', tags=self.tags)
        def read_by_hostname(hostname, offset=0, limit=100):
            vm = self.session.exec(select(self.model).where(self.model.hostname == hostname))
            return vm
        
        # GET /vm?name='vm1'
        @router.get(f'/{self.name}?'+'hostname={hostname}', tags=self.tags)
        def read_by_hostname(hostname, offset=0, limit=100):
            vm = self.session.exec(select(self.model).where(self.model.name == name))
            return vm
        
        # GET /vm/request
        @router.get(f'/{self.name}/request', tags=self.tags)
        def read_by_hostname(hostname, offset=0, limit=100):
            vm = self.session.exec(select(self.model).where(self.model.status == 'REQUEST'))
            return vm
        
        return router