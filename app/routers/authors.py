from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import crud
from ..schemas import AuthorCreate, AuthorOut, BookOut

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("", response_model=AuthorOut, status_code=201)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, payload)

@router.get("", response_model=list[AuthorOut])
def list_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return crud.list_authors(db, skip=skip, limit=limit)

@router.get("/{author_id}/books", response_model=list[BookOut])
def list_books_by_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    return author.books