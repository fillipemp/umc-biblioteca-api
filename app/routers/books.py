from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import crud
from ..schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.post("", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, payload)

@router.get("", response_model=list[BookOut])
def list_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    title: str | None = None,
    isbn: str | None = None,
):
    return crud.list_books(db, skip=skip, limit=limit, title=title, isbn=isbn)

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)

@router.put("/{book_id}", response_model=BookOut)
def put_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    return crud.update_book_put(db, book_id, payload)

@router.patch("/{book_id}", response_model=BookOut)
def patch_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book_patch(db, book_id, payload)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id)
    return None