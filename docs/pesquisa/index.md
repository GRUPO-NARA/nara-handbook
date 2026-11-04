# Pesquisa

A área de pesquisa do NARA produz estudos com dados públicos sobre o Maranhão. Cada pesquisa tem repositório próprio, criado a partir do `template-pesquisa`.

Antes de começar uma pesquisa nova, leia o [protocolo de pesquisa](protocolo.md).

!!! tip "Como atualizar"
    Esta tabela é gerada a partir de `data/pesquisas.yml`.

| Pesquisa | Status | Etapa | Equipe | Resultados |
|---|---|---|---|---|
{% for p in pesquisas -%}
| [{{ p.nome }}]({{ p.pagina | replace("pesquisa/", "") }}) | {{ status_pesquisa(p.status) }} | {{ etapa(p.etapa) }} | {{ nomes("membro", p.membros) }} | {{ ou_traco(p.resultados) }} |
{% endfor %}
