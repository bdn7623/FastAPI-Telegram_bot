from database import SessionLocal,Base,engine
from models import Lector,Group,Message
from fastapi import FastAPI
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from schemas import LectorView,GroupView,MessageView


app = FastAPI()

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()

Base.metadata.create_all(bind=engine)

lector_router = SQLAlchemyCRUDRouter(
    schema=LectorView,
    create_schema=LectorView,
    db_model=Lector,
    db=get_db,
    prefix='lector',
    get_all_route=False,
    get_one_route=False,
    delete_all_route=False,
    delete_one_route=False,
    update_route=False
)

group_router = SQLAlchemyCRUDRouter(
    schema=GroupView,
    create_schema=GroupView,
    db_model=Group,
    db=get_db,
    prefix='group',
    get_all_route=False,
    get_one_route=False,
    delete_all_route=False,
    delete_one_route=False,
    update_route=False
)

router_messages = SQLAlchemyCRUDRouter(
    schema=MessageView,
    create_schema=MessageView,
    db_model=Message,
    db=get_db,
    prefix='message',
    get_one_route=False,
    delete_all_route=False,
    delete_one_route=False,
    create_route=False,
    update_route=False
)

app.include_router(router_messages)
app.include_router(lector_router)
app.include_router(group_router)
