from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from uuid import UUID
from fastapi.param_functions import Header
from starlette.responses import JSONResponse

from book import Book, BookNoRating
from exceptions import NegativeNumberException

app = FastAPI()

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"mesage": f"Negative number exception for vaue {exception.books_to_return}"}
    )    

# passing form params example
@app.post("/books/login")   
async def books_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

# headers example
@app.get("/header")   
async def get_header(random_header: Optional[str] = Header(None)):
    return {"RandomHeader": random_header}


@app.get("/")
async def get_all_books(books_to_return: Optional[int] = None):
    
    if(books_to_return and books_to_return < 0):
        raise NegativeNumberException(books_to_return)

    if len(BOOKS) < 1:
        init_books()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        return BOOKS[:books_to_return]

    return BOOKS

@app.get("/book/{book_id}")
async def get_by_id(book_id: UUID):

    for book in BOOKS:
        if book.id == book_id:
            return book
    raise not_found_exception()

@app.get("/book/rating/{rating}", response_model=BookNoRating)
async def get_by_rating(rating: int):

    for book in BOOKS:
        if book.rating == rating:
            return book
    raise not_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id: UUID, updated_book: Book):
    for idx, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[idx] = updated_book
            return BOOKS[idx]
    raise not_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for idx, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[idx]
            return f"ID: {book_id} deleted"
    raise not_found_exception()

def init_books():
    book_1 = Book(id="71f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="21f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="31f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="41f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def not_found_exception():
    return HTTPException(status_code=404, detail="Book not found",
                                        headers={"X-Header-Error": "Book does not exist"})