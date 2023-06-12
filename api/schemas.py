from pydantic import BaseModel
from datetime import datetime
class LectorView(BaseModel):
    id:int
    username:str
    class Config:
        orm_mode = True

class GroupView(BaseModel):
    id:int
    group_name:str
    lectors:list[LectorView]
    class Config:
        orm_mode = True

        
class MessageView(BaseModel):
    id:int
    text:str
    link:str
    datetime:datetime.datetime
    groups:list[GroupView]
    class Config:
        orm_mode = True
