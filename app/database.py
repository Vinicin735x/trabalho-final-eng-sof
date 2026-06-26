from app.models import Livro


def init_db(db: dict) -> None:
    """Popula o banco com alguns livros de exemplo ao iniciar."""
    exemplos = [
        Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis",
              ano=1899, isbn="978-85-359-0277-5"),
        Livro(id=2, titulo="O Cortiço", autor="Aluísio Azevedo",
              ano=1890, isbn="978-85-260-0616-7"),
    ]
    for livro in exemplos:
        db[livro.id] = livro
