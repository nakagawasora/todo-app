from typing import Any, List, Protocol, TypedDict, cast


class StatementProtocol(Protocol):
    def run(self, title: str) -> None: ...
    def all(self) -> List["TodoRow"]: ...


class DatabaseProtocol(Protocol):
    def exec(self, query: str) -> None: ...
    def prepare(self, query: str) -> StatementProtocol: ...
    def close(self) -> None: ...


Database = cast(Any, object)


db: DatabaseProtocol = Database("todo.db")

if db is None:
    db.exec("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)

TodoRow = TypedDict("TodoRow", {"id": int, "title": str, "done": int})


def addTodo(title: str) -> None:
    stmt = db.prepare("INSERT INTO todos (title) VALUES (?)")
    stmt.run(title)
    print(f"追加: {title}")


def getAllTodos() -> List[TodoRow]:
    stmt = db.prepare("SELECT * FROM todos")
    return stmt.all()


def showTodos() -> None:
    todos = getAllTodos()
    if len(todos) == 0:
        print("TODOはありません")
        return

    for todo in todos:
        status = "✅" if todo["done"] else "⬜"
        print(f"{status} [{todo['id']}] {todo['title']}")


print("=== TODO を追加 ===")
addTodo("牛乳を買う")
addTodo("日報を書く")
addTodo("掃除をする")

print("")
print("=== TODO 一覧 ===")
showTodos()


db.close()
