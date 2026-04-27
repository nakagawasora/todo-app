import os
from schemas import TodoCreateRequest

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class TodoModel(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    done: Mapped[bool] = mapped_column(default=False, nullable=False)


class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@app.post("/api/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreateRequest, db: Session = Depends(get_db)):
    new_todo = TodoModel(title=todo.title, done=todo.done)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        return {"error": "Todo not found"}
    
    db_todo.done = not db_todo.done
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        return {"error": "Todo not found"}
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}


if os.path.exists("public"):
    app.mount("/", StaticFiles(directory="public", html=True), name="static")
