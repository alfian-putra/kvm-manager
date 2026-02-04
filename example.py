from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from sqlmodel import SQLModel


class Item(SQLModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

class ex():
    def __init__(self, model):
        self.model = model
    
    def router(self):
        router = APIRouter()

        @router.post("/items/")
        async def create_item(item: self.model):
            return item

        return router
        
example = ex(Item)

app.include_router(example.router())
        
