from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

class DirectionName(str, Enum):
    north = "north",
    south = "south",
    east = "east",
    west = "west"

# localhost:8000/?skip=book_1
@app.get("/")
async def get_all_books(skip: Optional[str] = None):
    if skip:
        new_books = BOOKS.copy()
        del new_books[skip]
        return new_books
    return BOOKS

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return BOOKS[f"book_{book_id}"]

@app.get("/{book_name}")
async def get_book(book_name: str):
    return BOOKS[book_name]

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.south:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.east:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.west:
        return {"Direction": direction_name}

@app.post("/")
async def create_book(book_title, book_author):
    book_name = "book_" + str(len(BOOKS) + 1)
    BOOKS[book_name] = {'title': book_title, 'author': book_author}
    return BOOKS
    

@app.put("/{book_name}")
async def update_book(book_name, book_title, book_author):
    BOOKS[book_name] = {'title': book_title, 'author': book_author}
    return BOOKS

@app.delete("/{book_name}")
async def delete_book(book_name:str):
    del BOOKS[book_name]
    return BOOKS
    

    