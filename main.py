from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas

# Crea la base de datos
Base.metadata.create_all(engine)

# Inicializa app
app = FastAPI()

@app.get("/")
def root():
    return "todooo"

@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo):

    # crear una seccion nueva en en la base de datos 
    session = Session(bind=engine, expire_on_commit=False)

    # crear uan instacia del modelo db 
    tododb = models.ToDo(task = todo.task)

    # Agregar
    session.add(tododb)
    session.commit()


    id = tododb.id

    #  cierra seccion
    session.close()

    # retorna el id
    return f"created todo item with id {id}"

@app.get("/todo/{id}")
def read_todo(id: int):

    # crear una seccion nueva en en la base de datos 
    session = Session(bind=engine, expire_on_commit=False)

    # obtienen id
    todo = session.query(models.ToDo).get(id)

    #  cierra seccion
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/todo/{id}")
def update_todo(id: int, task: str):

    # crear una seccion nueva en en la base de datos 
    session = Session(bind=engine, expire_on_commit=False)

    # gobtienen id
    todo = session.query(models.ToDo).get(id)

    # actualiza
    if todo:
        todo.task = task
        session.commit()

    #  cierra seccion
    session.close()


    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    # crear una seccion nueva en en la base de datos 
    session = Session(bind=engine, expire_on_commit=False)

    # obtienen id
    todo = session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/todo")
def read_todo_list():
    # crear una seccion nueva en en la base de datos 
    session = Session(bind=engine, expire_on_commit=False)

    # obtienen todas las tareas
    todo_list = session.query(models.ToDo).all()

    # cierra seccion
    session.close()

    return todo_list
