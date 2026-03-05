from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from .models import Author, Book
from .schemas import AuthorCreate, BookCreate, BookUpdate

# AUTHORS
def create_author(db: Session, data: AuthorCreate) -> Author:
    author = Author(name=data.name.strip())
    db.add(author)
    try:
        db.commit()
        db.refresh(author)
        return author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Autor já existe (nome duplicado).")

def list_authors(db: Session, skip: int = 0, limit: int = 20):
    stmt = select(Author).offset(skip).limit(limit).order_by(Author.name)
    return db.scalars(stmt).all()

def get_author(db: Session, author_id: int) -> Author:
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado.")
    return author

# BOOKS
def _load_authors_by_ids(db: Session, author_ids: list[int]) -> list[Author]:
    if not author_ids:
        return []
    stmt = select(Author).where(Author.id.in_(author_ids))
    authors = db.scalars(stmt).all()
    found_ids = {a.id for a in authors}
    missing = [i for i in author_ids if i not in found_ids]
    if missing:
        raise HTTPException(status_code=400, detail=f"Autor(es) não encontrado(s): {missing}")
    return authors

def create_book(db: Session, data: BookCreate) -> Book:
    authors = _load_authors_by_ids(db, data.author_ids)

    book = Book(
        title=data.title.strip(),
        publisher=(data.publisher.strip() if data.publisher else None),
        isbn=data.isbn,
        summary=data.summary,
        authors=authors,
    )
    db.add(book)
    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN já cadastrado.")

def list_books(db: Session, skip: int = 0, limit: int = 20, title: str | None = None, isbn: str | None = None):
    stmt = select(Book).offset(skip).limit(limit).order_by(Book.title)
    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if isbn:
        stmt = stmt.where(Book.isbn == isbn.replace("-", "").replace(" ", "").strip())
    return db.scalars(stmt).unique().all()

def get_book(db: Session, book_id: int) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return book

def update_book_put(db: Session, book_id: int, data: BookCreate) -> Book:
    book = get_book(db, book_id)
    authors = _load_authors_by_ids(db, data.author_ids)

    book.title = data.title.strip()
    book.publisher = data.publisher.strip() if data.publisher else None
    book.isbn = data.isbn
    book.summary = data.summary
    book.authors = authors

    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN já cadastrado em outro livro.")

def update_book_patch(db: Session, book_id: int, data: BookUpdate) -> Book:
    book = get_book(db, book_id)

    if data.title is not None:
        book.title = data.title.strip()
    if data.publisher is not None:
        book.publisher = data.publisher.strip() if data.publisher else None
    if data.isbn is not None:
        book.isbn = data.isbn
    if data.summary is not None:
        book.summary = data.summary
    if data.author_ids is not None:
        book.authors = _load_authors_by_ids(db, data.author_ids)

    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN já cadastrado em outro livro.")

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()