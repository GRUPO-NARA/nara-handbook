# Projetos

!!! tip "Como atualizar"
    Esta página é gerada a partir de `data/projetos.yml`.

**{{ contadores.projetos_andamento }}** em andamento · **{{ contadores.projetos_planejados }}** planejados · **{{ contadores.projetos_concluidos }}** concluídos

{% for p in projetos %}
## {{ p.nome }}

{{ p.descricao }}

| | |
|---|---|
| **Status** | {{ status_projeto(p.status) }} |
| **Categoria** | {{ ou_traco(p.categoria) }} |
| **Responsável** | {{ nome("membro", p.responsavel) if p.responsavel else "—" }} |
| **Parceiro** | {{ ou_traco(p.parceiro) }} |
| **Financiamento** | {{ ou_traco(p.financiamento) }} |
| **Stack** | {{ ou_traco(p.stack) }} |
| **Repositório** | {% if p.repositorio %}[GRUPO-NARA/{{ p.repositorio }}](https://github.com/GRUPO-NARA/{{ p.repositorio }}){% else %}—{% endif %} |
| **Link** | {% if p.url %}<{{ p.url }}>{% else %}—{% endif %} |

{% endfor %}
