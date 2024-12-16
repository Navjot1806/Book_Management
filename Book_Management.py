from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Create an instance of the FastAPI application
app = FastAPI()

# Define a Pydantic model for book data validation
class Book(BaseModel):
    id: int                # Unique identifier for the book
    title: str             # Title of the book
    author: str            # Author of the book
    year: int              # Year the book was published
    available: bool        # Availability status of the book

# In-memory storage for books (simulates a database)
books = []

# Root endpoint to welcome users
@app.get("/")
def root():
    return {"message": "Welcome to the Book Management System!"}

# Endpoint to add a new book
@app.post("/books/", response_model=Book)
def add_book(book: Book):
    # Check if the book ID already exists
    for existing_book in books:
        if existing_book.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    
    # Add the book to the in-memory storage
    books.append(book)
    return book

# Endpoint to retrieve all books
@app.get("/books/", response_model=List[Book])
def get_books():
    print('retrieving the information for books')
    return books

# Endpoint to get a specific book by its ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    # Search for the book by ID
    for book in books:
        if book.id == book_id:
            print('return the book information if the id of books are same')
            return book

    # If not found, raise an exception
    raise HTTPException(status_code=404, detail="Book not found")

# Endpoint to update an existing book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    # Iterate over the books to find the match
    for index, book in enumerate(books):
        if book.id == book_id:
            # Update the book details
            books[index] = updated_book
            return updated_book

    # If not found, raise an exception
    raise HTTPException(status_code=404, detail="Book not found")

# Endpoint to delete a book by its ID
@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int):
    # Search for the book by ID
    for index, book in enumerate(books):
        if book.id == book_id:
            # Remove the book from the list
            del books[index]
            return {"message": "Book deleted successfully"}

    # If not found, raise an exception
    raise HTTPException(status_code=404, detail="Book not found")
