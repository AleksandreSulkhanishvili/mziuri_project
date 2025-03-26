from ninja import Schema
from datetime import datetime
from typing import List, Optional


class GenreSchema(Schema):
    id: int
    name: str
    description: Optional[str] = None


class BookSchema(Schema):
    id: int
    title: str
    author: str
    published_date: datetime
    genres: List[GenreSchema]
    borrowed_by: Optional[str] = None
    borrow_date: Optional[datetime] = None
    is_borrowed: bool


class BookCreateSchema(Schema):
    title: str
    author: str
    published_date: Optional[datetime] = None
    genre_id: List[int]


class BookUpdateSchema(Schema):
    title: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    genre_id: Optional[List[int]] = None


class BorrowCreateSchema(Schema):
    person: str
