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

## Dados do laboratório

Membros, projetos e pesquisas ficam em `data/` e geram as páginas automaticamente:

| Arquivo | O que guarda |
|---|---|
| `data/laboratorio.yml` | Nome oficial, contato e links |
| `data/membros.yml` | Membros e status (ativo, nivelamento, egresso) |
| `data/projetos.yml` | Projetos de software |
| `data/pesquisas.yml` | Pesquisas |
| `data/github.yml` | Labels e campos do GitHub Projects |

Para aplicar labels e campos do Projects na organização:

```bash
gh auth refresh -s project,read:org
python scripts/configurar_github.py --simular
python scripts/configurar_github.py
```

Para publicar os issue templates e o template de PR no repositório `GRUPO-NARA/.github` (origem: `templates-organizacao/.github/`):

```bash
bash scripts/publicar_templates.sh
```

Os campos aceitos estão descritos no topo de cada arquivo. Se um id citado não existir ou um status for inválido, o build falha e mostra o erro.

Os mesmos dados são publicados em JSON para o site institucional:
`/api/laboratorio.json`, `/api/membros.json`, `/api/projetos.json`, `/api/pesquisas.json`.

## Como contribuir

1. Crie uma branch: `docs/nome-da-mudanca`
2. Edite os arquivos em `docs/`
3. Abra um PR. O GitHub Actions verifica se o build continua passando.

Toda página nova precisa entrar no `nav` do `mkdocs.yml`.
