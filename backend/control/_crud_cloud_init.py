# appending Crud() object with more specific functionality for model : disk
import os
import json

from fastapi import APIRouter, \
                    HTTPException
from pydantic import BaseModel
from sqlmodel import select
from ..lib.vm_utility import cloud_init_create, \
                             render_template, \
                             const_value
from ._crud import Crud
from ..model.model import Vm, Os, CloudInit, CloudInitContent
from ..lib.common_utility import log, config

class CrudCloudInit(Crud):
    def __init__(self, model, 
                       name=''):
        Crud.__init__(self, 
                      model,
                      name)
        self.router = Crud.get_router(self)
    ## GET /cloud_init/content/filename.tmp     get content
    ## POST /cloud_init/content/filename.tmp    post content
    ## GET /cloud_init/content/generate/filename.tmp?vmId=1     get content 
    # {
    #     "filename" : "filename.tmp",
    #     "content" : "hostname: {hostname}"
    #     "vars: {'hostname':'hostname.example.com'}"
    # }
    ## PUT /cloud_init/content/filename.tmp     update 
    def get_router(self):
        router = self.router
        
        @router.get(f'/const_value', tags=self.tags)
        def get_const_value():
            return const_value()
        
        @router.get(f'/{self.name}/content/'+'{filename}', tags=self.tags)
        def cloud_init_get_model_and_content(filename, session:self.session):
            res = ""
            try:
                cloud_init_model = session.exec(select(self.model).where(self.model.filename == filename)).first()
                log.info(cloud_init_model)
                content = ""
                cloud_init_file = filename if "tmp" in filename else os.path.join(config["backend"]["cloud_init"]["tmp"],filename)
                with open(cloud_init_file, "r") as f:
                    content = f.read()
                res =  {"filename":filename, "content":content, "vars":cloud_init_model.vars}
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))
            return res
        
        @router.post(f'/{self.name}/content', tags=self.tags)
        def cloud_init_post_content(session: self.session, new_entity:CloudInitContent):
            try:
                _data = CloudInit(filename=new_entity.filename, vars=new_entity.vars)
                session.add(_data)
                session.commit()
                session.refresh(_data)
                cloud_init_file = new_entity.filename if "tmp" in new_entity.filename else os.path.join(config["backend"]["cloud_init"]["tmp"],new_entity.filename)
                with open(cloud_init_file, "w") as f:
                    f.write(new_entity.content)
            except Exception as e:
                raise HTTPException(status_code=404, detail={"status": e})
            return {'status' : 'success'}
        
        @router.get(f'/{self.name}/content/generate/'+'{filename}?vmId={vm_id}', tags=self.tags)
        def cloud_init_generate(filename,vm_id):
            cloud_init_model = self.session.exec(select(self.model).where(self.model.filename == filename))
            vm =  self.session.exec(select(Vm).where(Vm.id == vm_id))
            os_data =  self.session.exec(select(Vm).where(Os.id == vm.os_id))
            filepath = filename if "tmp" in filename else os.path.join(config["backend"]["cloud_init"]["tmp"],filename)
            content = ""
            with open(filepath, "r") as f:
                content = f.readlines()
            generated_file= render_template(cloud_init_model["filename"],cloud_init_model["vars"],vm=vm,os_data=os_data)
            
            return {"filename":generated_file}
        
        @router.patch(f'/{self.name}/content/'+'{id}', tags=self.tags)
        def cloud_init_update_content(session:self.session,id, entity: CloudInitContent):
            # {
            #     "filename" : "filename.tmp",
            #     "content" : "hostname: {hostname}"
            #     "vars: {'hostname':'hostname.example.com'}"
            # }
            
            db_data = session.exec(select(self.model).where(self.model.id == id)).first()
            _id = db_data.id
            _data = CloudInit(filename=entity.filename, vars=entity.vars)
            db = session.get(self.model, _id)
            if not db:
                raise HTTPException(status_code=404, detail="data not found")
            data = _data.model_dump(exclude_unset=True)
            db.sqlmodel_update(data)
            session.add(db)
            session.commit()
            session.refresh(db)

            filepath = db_data.filename if "tmp" in db_data.filename else os.path.join(config["backend"]["cloud_init"]["tmp"],db_data.filename)
            
            with open(filepath, "w") as f: 
                f.write(entity.content)
        
            return {"status":"success"}

        return router