from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# AUTHORS
class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)

class AuthorOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# BOOKS
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=250)
    publisher: Optional[str] = Field(None, max_length=200)
    isbn: str = Field(..., min_length=10, max_length=32)
    summary: Optional[str] = None
    author_ids: List[int] = Field(default_factory=list, description="IDs dos autores")

    @field_validator("isbn")
    @classmethod
    def normalize_isbn(cls, v: str) -> str:
        return v.replace("-", "").replace(" ", "").strip()

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=250)
    publisher: Optional[str] = Field(None, max_length=200)
    isbn: Optional[str] = Field(None, min_length=10, max_length=32)
    summary: Optional[str] = None
    author_ids: Optional[List[int]] = None 

    @field_validator("isbn")
    @classmethod
    def normalize_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.replace("-", "").replace(" ", "").strip()

class BookOut(BaseModel):
    id: int
    title: str
    publisher: Optional[str]
    isbn: str
    summary: Optional[str]
    authors: List[AuthorOut]

    class Config:
        from_attributes = True