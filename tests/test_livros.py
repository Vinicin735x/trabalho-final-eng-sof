import pytest
from fastapi.testclient import TestClient
from app.main import app, _db


@pytest.fixture(autouse=True)
def limpar_banco():
    """Reseta o estado do banco antes de cada teste."""
    _db.clear()
    # Importa e reseta o contador de IDs
    import app.main as m
    m._next_id = 1
    yield
    _db.clear()


client = TestClient(app)


# ── Testes de criação ────────────────────────────────────────────────────────
def test_criar_livro():
    payload = {
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949,
        "isbn": "978-0-452-28423-4",
    }
    response = client.post("/livros", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "1984"
    assert data["id"] == 1


def test_criar_livro_campos_invalidos():
    """Título vazio deve retornar 422 (Unprocessable Entity)."""
    payload = {"titulo": "", "autor": "X", "ano": 2000, "isbn": "1234567890"}
    response = client.post("/livros", json=payload)
    assert response.status_code == 422


# ── Testes de leitura ────────────────────────────────────────────────────────
def test_listar_livros_vazio():
    response = client.get("/livros")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_livros_com_dados():
    client.post("/livros", json={
        "titulo": "Cem Anos de Solidão",
        "autor": "Gabriel García Márquez",
        "ano": 1967,
        "isbn": "978-0-06-088328-7",
    })
    response = client.get("/livros")
    assert len(response.json()) == 1


def test_buscar_livro_existente():
    client.post("/livros", json={
        "titulo": "Cem Anos de Solidão",
        "autor": "Gabriel García Márquez",
        "ano": 1967,
        "isbn": "978-0-06-088328-7",
    })
    response = client.get("/livros/1")
    assert response.status_code == 200
    assert response.json()["autor"] == "Gabriel García Márquez"


def test_buscar_livro_inexistente():
    response = client.get("/livros/999")
    assert response.status_code == 404


# ── Testes de atualização ────────────────────────────────────────────────────
def test_atualizar_livro():
    client.post("/livros", json={
        "titulo": "Titulo Antigo",
        "autor": "Autor",
        "ano": 2000,
        "isbn": "1234567890",
    })
    response = client.put("/livros/1", json={
        "titulo": "Titulo Novo",
        "autor": "Autor",
        "ano": 2000,
        "isbn": "1234567890",
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Titulo Novo"


def test_atualizar_livro_inexistente():
    response = client.put("/livros/999", json={
        "titulo": "X", "autor": "Y", "ano": 2000, "isbn": "1234567890"
    })
    assert response.status_code == 404


# ── Testes de remoção ────────────────────────────────────────────────────────
def test_deletar_livro():
    client.post("/livros", json={
        "titulo": "Para deletar",
        "autor": "Autor",
        "ano": 2020,
        "isbn": "1234567890",
    })
    response = client.delete("/livros/1")
    assert response.status_code == 204
    # Confirma que sumiu
    assert client.get("/livros/1").status_code == 404


def test_deletar_livro_inexistente():
    response = client.delete("/livros/999")
    assert response.status_code == 404
