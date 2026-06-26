# 📚 Cadastro de Livros — Grupo 3 (Build e CI)

Aplicação CRUD de livros desenvolvida com **FastAPI** para demonstrar
os conceitos de **Build** e **Integração Contínua (CI)** com **GitHub Actions**.

## 🚀 Como rodar localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o servidor
uvicorn app.main:app --reload

# 3. Acessar a documentação automática
# http://localhost:8000/docs
```

## 🧪 Rodando os testes

```bash
# Rodar todos os testes
pytest tests/ -v

# Com relatório de cobertura
pytest tests/ -v --cov=app --cov-report=term-missing
```

## 🔍 Lint

```bash
flake8 app/ tests/ --max-line-length=100
```

## ⚙️ Pipeline de CI (GitHub Actions)

O pipeline é disparado automaticamente a cada `push` ou `pull request` e executa:

1. **Checkout** — baixa o código
2. **Setup Python** — configura o ambiente
3. **Install** — instala as dependências
4. **Lint** — verifica qualidade do código com `flake8`
5. **Tests** — roda os testes com `pytest` e exibe cobertura

## 📁 Estrutura do projeto

```
crud-livros/
├── app/
│   ├── main.py       # Rotas da API
│   ├── models.py     # Modelos Pydantic
│   └── database.py   # Inicialização dos dados
├── tests/
│   └── test_livros.py
├── .github/
│   └── workflows/
│       └── ci.yml    # Pipeline GitHub Actions
└── requirements.txt
```
