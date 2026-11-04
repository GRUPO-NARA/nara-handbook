# Membros

!!! tip "Como atualizar"
    Esta página é gerada a partir de `data/membros.yml`. Para entrar, sair ou mudar de função, edite esse arquivo e abra um PR.

**{{ contadores.membros_ativos }}** membros ativos{% if contadores.em_nivelamento %} · **{{ contadores.em_nivelamento }}** em nivelamento{% endif %}

## Ativos

| Nome | Função | Área | Projetos | Pesquisas |
|---|---|---|---|---|
{% for m in membros if m.status == "ativo" -%}
| {% if m.github %}[{{ m.nome }}](https://github.com/{{ m.github }}){% else %}{{ m.nome }}{% endif %} | {{ ou_traco(m.funcao) }} | {{ area(m.area) }} | {{ nomes("projeto", m.projetos) }} | {{ nomes("pesquisa", m.pesquisas) }} |
{% endfor %}

{% set niv = membros | selectattr("status", "equalto", "nivelamento") | list %}
{% if niv %}
## Em nivelamento

| Nome | Entrada |
|---|---|
{% for m in niv -%}
| {{ m.nome }} | {{ ou_traco(m.entrada) }} |
{% endfor %}
{% endif %}

{% set egr = membros | selectattr("status", "equalto", "egresso") | list %}
{% if egr %}
## Egressos

{% for m in egr -%}
- {{ m.nome }}
{% endfor %}
{% endif %}
