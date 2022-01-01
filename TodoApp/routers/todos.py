import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
from todo import Todo
from db import get_db
import models
from db import engine
from sqlalchemy.orm import Session
from security import get_current_user, get_user_exception

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

models.db_base.metadata.create_all(bind=engine)

@router.get("/")
async def get_all(database:Session = Depends(get_db)):
    return database.query(models.Todos).all()

@router.get("/user")
async def get_by_user(user: dict = Depends(get_current_user), database:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    return database.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def get_by_id(todo_id: int, user: dict = Depends(get_current_user), database:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = database.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id")).first()

    if todo_model is not None:
        return todo_model
    raise not_found_exception()

@router.post("/")
async def create_todo(todo: Todo,
                    user: dict = Depends(get_current_user),
                    database:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    database.add(todo_model)
    database.commit()

    return successful_response(201)

@router.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user), 
                      database:Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()
    
    todo_model = database.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        raise not_found_exception()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    database.add(todo_model)
    database.commit()

    return successful_response(200)

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      database:Session = Depends(get_db)):
    
    if user is None:
        raise get_user_exception()

    todo_model = database.query(models.Todos)\
                .filter(models.Todos.id == todo_id)\
                .filter(models.Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        raise not_found_exception()

    database.delete(todo_model)
    database.commit()

    return successful_response(201)

def not_found_exception():
    return HTTPException(status_code=404, detail="Todo not found")

def successful_response(status_code: int):
     return {
        "status": status_code,
        "transaction": "Successful"
    }
