import json

from fastapi import APIRouter, \
                    HTTPException, \
                    Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlmodel import select

from ..lib.common_utility import session
from ..lib.jwt_handler import verify_jwt

router = APIRouter()

class Crud():
    def __init__(self, model, name=''):
        # session same as SessionDep from example
        self.model = model
        self.name = name
        self.session = session
        self.tags=[self.name]
        self.dependency= { "verify_jwt" : verify_jwt}

    # if self.name='user' will produce this api
    #
    # CREATE  POST      /user
    # READ    GET       /user?id=1
    # READ    GET       /user
    # UPDATE  PUT       /user?id=1
    # DELETE  DELETE    /user?id=1
    def get_router(self):
        router = APIRouter()

        @router.get(f"/{self.name}/model", tags=self.tags)
        def get_model():
            return json.loads(self.model.structure())
        
        @router.post(f'/{self.name}', tags=self.tags)
        def create(new_entity: self.model, session: self.session):
            session.add(new_entity)
            session.commit()
            session.refresh(new_entity)
            return new_entity

        @router.get(f'/{self.name}/' + '{id}', tags=self.tags) # /model?id=1
        def read(id, session: self.session):
            # statement = select(self.model).where(self.model.id == id)
            # result = session.exec(statement)
            # print(result)
            db = session.get(self.model, id)
            if db is None:
                raise HTTPException(status_code=404, detail=f"{self.name} not found")
            return db
        
        @router.get(f'/{self.name}', tags=self.tags)
        def read_all(session: self.session, offset=0, limit=100):
            statement = select(self.model)
            result = session.exec(statement)
            return result.all()
        
        @router.patch(f'/{self.name}/' + '{id}', tags=self.tags, response_model=self.model) # /model?id=1
        def update(id, new_entity: self.model, session: self.session):
            db = session.get(self.model, id)
            if not db:
                raise HTTPException(status_code=404, detail="data not found")
            data = new_entity.model_dump(exclude_unset=True)
            db.sqlmodel_update(data)
            session.add(db)
            session.commit()
            session.refresh(db)
            return db
        
        @router.delete(f'/{self.name}/' + '{id}', tags=self.tags) # /model?id=1
        def delete(id, session: self.session):
            entity = session.get(self.model, id)
            if not entity:
                raise HTTPException(status_code=404, detail=f"{self.name} not found")
            session.delete(entity)
            session.commit()

            return {"status": True}

        
        return router