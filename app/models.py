from pydantic import BaseModel, Field


class LivroCreate(BaseModel):
    """Dados necessários para criar ou atualizar um livro."""
    titulo: str = Field(..., min_length=1, max_length=200, examples=["Dom Casmurro"])
    autor: str = Field(..., min_length=1, max_length=100, examples=["Machado de Assis"])
    ano: int = Field(..., ge=1000, le=2100, examples=[1899])
    isbn: str = Field(..., min_length=10, max_length=17, examples=["978-85-359-0277-5"])


class Livro(LivroCreate):
    """Livro completo, com ID gerado pelo sistema."""
    id: int
