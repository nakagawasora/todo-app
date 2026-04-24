import asyncio
import httpx
from typing import List, TypedDict

# --- 型定義 (TypeScriptの TodoFromAPI に相当) ---
class TodoFromAPI(TypedDict):
    userId: int
    id: int
    title: str
    completed: bool

async def fetch_todos() -> None:
    print("APIからTODOを取得中...")

    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos?_limit=5")
        
        # response.json() は Python のリスト/辞書に変換される
        todos: List[TodoFromAPI] = response.json()

    print(f"{len(todos)} 件取得しました")
    print("")

    for todo in todos:
        status = "✅" if todo["completed"] else "⬜"
        print(f"{status} [{todo['id']}] {todo['title']}")

# --- 実行部分 ---
# Pythonでは最上位レベルで await が使えないため、run で起動します
if __name__ == "__main__":
    asyncio.run(fetch_todos())