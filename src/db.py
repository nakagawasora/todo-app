from sqlite3 import Database
from typing import List, TypedDict


db = Database("todo.db")

db.exec(`
  CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
  )
`);

TodoRow = TypedDict("TodoRow", {"id": int, "title": str, "done": int})

def addTodo(title: str) -> None:
  stmt = db.prepare("INSERT INTO todos (title) VALUES (?)");
  stmt.run(title);
  print(f"追加: {title}");

def getAllTodos() -> List[TodoRow]:
  stmt = db.prepare("SELECT * FROM todos");
  return stmt.all() as List[TodoRow];

def showTodos() -> None:
  todos = getAllTodos();
  if (todos.length === 0):
    print("TODOはありません");
    return;

  for (const todo of todos) {
    const status = todo.done ? "✅" : "⬜";
    print(f"{status} [{todo.id}] {todo.title}");
  }
};

print("=== TODO を追加 ===");
addTodo("牛乳を買う");
addTodo("日報を書く");
addTodo("掃除をする");

print("");
print("=== TODO 一覧 ===");
showTodos();


db.close();
