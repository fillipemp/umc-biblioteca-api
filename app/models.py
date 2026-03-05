from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)

class Author(Base):
    __tablename__ = "authors"
    __table_args__ = (UniqueConstraint("name", name="uq_authors_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    books = relationship("Book", secondary=book_authors, back_populates="authors")

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("isbn", name="uq_books_isbn"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    publisher: Mapped[str | None] = mapped_column(String(200), nullable=True)
    isbn: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    authors = relationship("Author", secondary=book_authors, back_populates="books")