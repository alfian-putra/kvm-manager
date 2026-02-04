# appending Crud() object with more specific functionality for model : user
from fastapi import APIRouter, \
                    HTTPException
from pydantic import BaseModel
from sqlmodel import select
from passlib.context import CryptContext

from ._crud import Crud
from ..model.model import CloudInit
from ..lib.common_utility import log
from ..lib.auth_handler import verify_password, get_password_hash
from ..lib.jwt_handler import signJWT, decodeJWT

class CrudUser(Crud):
    def __init__(self, model, 
                       name=''):
        Crud.__init__(self, 
                      model,
                      name)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.router = Crud.get_router(self)

    def get_router(self):
        router = self.router

        # GET /user?user_id={user_id}
        @router.get(f'/{self.name}/' + 'user_id/{user_id}', tags=self.tags)
        def read_by_user_id(user_id: str, session: self.session):
            statement = select(self.model).where(self.model.user_id==user_id)
            res = session.execute(statement)            
            user = res.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=404, detail="data not found")
            return user 
        
        # GET /user?name={name}
        @router.get(f'/{self.name}/' + 'username/{username}', tags=self.tags)
        def read_by_username(username, session: self.session, offset=0, limit=100):
            user = session.exec(select(self.model).where(self.model.username == username))
            print(user)
            if user is None:
                raise HTTPException(status_code=404, detail="data not found")
            
            return user 

        # POST /user/hashing_password={password}
        @router.post(f'/{self.name}/hashing_password='+ "{password}", tags=self.tags)
        def hashing_password(password):
            return get_password_hash(password)
        
        # POST /user/authenticate/name={name}&password={password}
        @router.get(f'/{self.name}/authenticate/' + 'username={username}&password={password}', tags=self.tags)
        def authenticate(username, password, session: self.session, offset=0, limit=100):
            user = session.exec(select(self.model).where(self.model.username == username)).first()

            if not user:
                return HTTPException(status_code=404, detail=f"{self.name} not found !")
            if not verify_password(password, get_password_hash(user.password)):
                return HTTPException(status_code=404, detail=f"authentication failed : wrong username or password !")
            
            token = signJWT(user.id)

            return {"access_token" : token}
        
        # POST /user/authenticate/user_id={user_id}&token={token}
        @router.post(f'/{self.name}/authenticate/'+"validate_token={token}", tags=self.tags)
        def validate_token(token):
            decoded_token = decodeJWT(token)

            log.info(f"Decoding token : {token}")
            log.debug(f"Decoded_token : {decoded_token}")
            # if decoded_token["user_id"]==user_id:
            #     return {"is_valid" : True}
            if decoded_token==None:
                return {"is_valid" : False}
            return {"is_valid" : True}
        
        @router.post(f'/{self.name}/init', tags=self.tags)
        def init(session: self.session):
            default = CloudInit(filename="default", vars="hostname:_HOSTNAME")
            session.add(default)
            session.commit()
            session.refresh(default)
            return default
        return router