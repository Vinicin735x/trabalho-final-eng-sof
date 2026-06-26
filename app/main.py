from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.models import Livro, LivroCreate

app = FastAPI(
    title="Cadastro de Livros",
    description="CRUD simples de livros — Grupo 3 (Build e CI)",
    version="1.0.0",
)

# Banco em memória simples (dict) para não precisar de ORM na demo
_db: dict[int, Livro] = {}
_next_id = 1


@app.on_event("startup")
def startup():
    init_db(_db)


# ── CREATE ──────────────────────────────────────────────────────────────────
@app.post("/livros", response_model=Livro, status_code=201)
def criar_livro(dados: LivroCreate):
    global _next_id
    livro = Livro(id=_next_id, **dados.model_dump())
    _db[_next_id] = livro
    _next_id += 1
    return livro


# ── READ (lista) ─────────────────────────────────────────────────────────────
@app.get("/livros", response_model=list[Livro])
def listar_livros():
    return list(_db.values())


# ── READ (único) ─────────────────────────────────────────────────────────────
@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    if livro_id not in _db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return _db[livro_id]


# ── UPDATE ───────────────────────────────────────────────────────────────────
@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, dados: LivroCreate):
    if livro_id not in _db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    _db[livro_id] = Livro(id=livro_id, **dados.model_dump())
    return _db[livro_id]


# ── DELETE ───────────────────────────────────────────────────────────────────
@app.delete("/livros/{livro_id}", status_code=204)
def deletar_livro(livro_id: int):
    if livro_id not in _db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    del _db[livro_id]
