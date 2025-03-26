from ninja import Router, Schema, Query
from django.shortcuts import get_object_or_404
from .models import Book, Genre
from .serializers import BookSchema, BookCreateSchema, BookUpdateSchema
from typing import Optional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication

router = Router()


@router.post("/token")
def get_token(request, username: str, password: str):
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    return {"error": "Invalid credentials"}, 401


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
            return user
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None


"""AUTH ROUTER"""


class BookFilter(Schema):
    genre: Optional[str] = None
    borrowed_by: Optional[str] = None
    borrowed: Optional[bool] = None


@router.get("/books", response=list[BookSchema], security=[JWTBearer()])
def get_books(request, filters: BookFilter = Query(...)):
    books = Book.objects.all()

    if filters.genre:
        books = books.filter(genres__name=filters.genre)

    if filters.borrowed_by:
        books = books.filter(borrowed_by=filters.borrowed_by)

    if filters.borrowed is not None:
        books = books.filter(borrowed_by__isnull=not filters.borrowed)

    return [BookSchema.from_orm(book) for book in books]


@router.get("/books/{book_id}", response=BookSchema, security=[JWTBearer()])
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)


@router.post("/books", response=BookSchema, security=[JWTBearer()])
def create_book(request, payload: BookCreateSchema):
    book = Book.objects.create(
        title=payload.title,
        author=payload.author,
        published_date=payload.published_date,
    )
    book.genres.set(Genre.objects.filter(id__in=payload.genre_ids))
    return book


@router.put("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int, payload: BookUpdateSchema):
    book = get_object_or_404(Book, id=book_id)

    if payload.title:
        book.title = payload.title
    if payload.author:
        book.author = payload.author
    if payload.published_date:
        book.published_date = payload.published_date
    if payload.genre_ids:
        book.genres.set(Genre.objects.filter(id__in=payload.genre_ids))

    book.save()
    return book


@router.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"response": "წიგნი წარმატებით წაიშალა"}


@router.post("/books/{book_id}/borrow", response=BookSchema)
def borrow_book(request, book_id: int, payload: BorrowCreateSchema):
    book = get_object_or_404(Book, id=book_id)
    if book.borrowed_by:
        return {"Error": "წიგნი უკვე გამოტანილია"}
    book.borrow(payload.person)
    return book


@router.post("/books/{book_id}/return")
def return_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    if not book.borrowed_by:
        return {"message": "წიგნი გამოტანილი არაა"}
    book.return_book()
    return {"message": "წიგნი წარმატებით დაბრუნებულია!"}
