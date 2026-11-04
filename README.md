# NARA — Handbook

Guia interno do NARA (LEA · UEMA): membros, stack, processo, nivelamento, projetos e pesquisa.

Publicado em: https://handbook.nucleonara.tech

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Acesse http://127.0.0.1:8000. As páginas recarregam sozinhas ao salvar.

## Como contribuir

1. Crie uma branch: `docs/nome-da-mudanca`
2. Edite os arquivos em `docs/`
3. Abra um PR. O GitHub Actions verifica se o build continua passando.

Toda página nova precisa entrar no `nav` do `mkdocs.yml`.
