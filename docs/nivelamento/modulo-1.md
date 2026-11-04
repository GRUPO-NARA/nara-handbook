# Módulo 1 — Python e análise de dados

Base de programação e de análise de dados que todo projeto do NARA usa. Você estuda no seu ritmo.

## Parte A — Python, do básico à POO

- **Vídeos:** playlist [Minicurso de Python](https://www.youtube.com/playlist?list=PLoATWfpSJDv8EFtRnTZmarWyQrT8xNuNS) (10 aulas)
- **Material de apoio:** repositório [minicurso-python](https://github.com/GRUPO-NARA/minicurso-python)

!!! note "Sobre o nome nos vídeos"
    Os vídeos aparecem como *Synapse Lab*, o nome antigo do laboratório. O conteúdo é o mesmo.

Conteúdo: sintaxe, variáveis e tipos, estruturas de controle, funções, estruturas de dados e Programação Orientada a Objetos.

## Parte B — Análise de dados

- **Material:** repositório [minicurso-de-analise-de-dados](https://github.com/GRUPO-NARA/minicurso-de-analise-de-dados)

Siga esta ordem, que é a mesma do README do repositório:

| # | Aula | Arquivo | O que aprende |
|---|---|---|---|
| 1 | NumPy | `aulas/numpy/main.py` | Arrays e operações numéricas |
| 2 | Pandas | `aulas/pandas/main.ipynb` | Ler CSV, selecionar, filtrar, estatísticas |
| 3 | Tratamento de dados | `aulas/tratamento-de-dados/arquivo_de_tratamento.ipynb` | Limpar e transformar uma base |
| 4 | Streamlit | `aulas/streamlit/main.py` | Dashboard com dados de saúde dos municípios do MA |

```bash
git clone https://github.com/GRUPO-NARA/minicurso-de-analise-de-dados
cd minicurso-de-analise-de-dados
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run aulas/streamlit/main.py
```

Depois de rodar o dashboard, **modifique-o**: troque um gráfico, adicione um filtro, use outra coluna. Mexer no código é a melhor forma de fixar.

## Checklist

- [ ] Assisti às 10 aulas da playlist
- [ ] Rodei os exemplos do `minicurso-python`
- [ ] Rodei a aula de NumPy
- [ ] Fiz o notebook de Pandas
- [ ] Fiz o notebook de tratamento de dados
- [ ] Rodei e modifiquei o dashboard em Streamlit

## Critério de aprovação

!!! warning "A definir pela coordenação"
    Descreva aqui como o módulo 1 é aprovado (por exemplo: conversa com o padrinho, exercício prático, mini dashboard próprio).

A data de aprovação é registrada na issue de nivelamento. **O prazo de 1 mês do [módulo 2](modulo-2.md) começa a contar a partir dela.**
