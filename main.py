from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from pydantic import BaseModel

# --- 1. データベース設定 ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# --- 2. データベースのテーブル定義 (SQLAlchemy) ---
class TodoModel(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    done: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(bind=engine)


# --- 3. APIのデータ構造定義 (Pydantic) ---
# TypeScript の type Todo = { ... } に相当
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True


# --- 4. FastAPI本体 ---
app = FastAPI()


# データベースセッションを取得する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    # SQLを書かずにデータを取得できる
    return db.query(TodoModel).all()
