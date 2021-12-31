from fastapi import FastAPI, Depends, HTTPException
from todo import Todo
from db import get_db
import models
from db import engine
from sqlalchemy.orm import Session


app = FastAPI()

models.db_base.metadata.create_all(bind=engine)

@app.get("/")
async def get_all(database:Session = Depends(get_db)):
    return database.query(models.Todos).all()

@app.get("/todo/{todo_id}")
async def get_by_id(todo_id: int, database:Session = Depends(get_db)):
    todo_model = database.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise not_found_exception()

@app.post("/todo/")
async def create_todo(todo: Todo, database:Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    database.add(todo_model)
    database.commit()

    return successful_response(201)

@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, database:Session = Depends(get_db)):
    
    todo_model = database.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise not_found_exception()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    database.add(todo_model)
    database.commit()

    return successful_response(200)

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, database:Session = Depends(get_db)):
    
    todo_model = database.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .first()

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
