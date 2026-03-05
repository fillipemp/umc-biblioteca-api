from fastapi import FastAPI
from .db import engine, Base
from .routers import authors, books

def create_app() -> FastAPI:
    app = FastAPI(
        title="UMC Biblioteca API",
        version="1.0.0",
        description="API RESTful para cadastro e controle de livros e autores."
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(authors.router)
    app.include_router(books.router)

    return app

app = create_app()