from typing import List, TypedDict

# --- Todo 型を定義する ---
class Todo(TypedDict):
    id: int
    title: str
    done: bool

# --- Todo の配列を作成する ---
todos: List[Todo] = [
    {"id": 1, "title": "牛乳を買う", "done": False},
    {"id": 2, "title": "日報を書く", "done": True},
    {"id": 3, "title": "TypeScriptを学ぶ", "done": False},
]

# --- 一覧を表示する関数 ---
def show_todos(todos: List[Todo]) -> None:
    for todo in todos:
        status = "✅" if todo["done"] else "⬜"
        print(f"{status} [{todo['id']}] {todo['title']}")


print("=== TODO 一覧 ===")
show_todos(todos)

def add_todo(todos: List[Todo], title: str) -> List[Todo]:
  newId = len(todos) + 1
  newTodo: Todo = { "id": newId, "title": title, "done": False }
  return todos + [newTodo]

updatedTodos = add_todo(todos, "掃除をする")

print("")
print("=== 追加後の TODO 一覧 ===")
show_todos(updatedTodos)