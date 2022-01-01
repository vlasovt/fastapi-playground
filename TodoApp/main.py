from fastapi import FastAPI, Depends
import models
from db import engine
from routers import auth, todos
from company import companyapis, dependencies

app = FastAPI()

models.db_base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418:{"description": "Internal use only"}}
)