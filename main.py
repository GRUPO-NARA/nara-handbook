"""
Módulo do mkdocs-macros: carrega os arquivos de data/, valida as referências
entre eles e expõe variáveis e funções para as páginas Markdown.

Também exporta os dados como JSON em /api/*.json no site publicado,
para o site institucional consumir (passo 7).
"""

import json
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).parent / "data"

STATUS_PROJETO = {
    "planejado": "🟡 Planejado",
    "em-andamento": "🟢 Em andamento",
    "pausado": "⏸️ Pausado",
    "concluido": "✅ Concluído",
}
STATUS_PESQUISA = {
    "planejada": "🟡 Planejada",
    "em-andamento": "🟢 Em andamento",
    "concluida": "✅ Concluída",
}
STATUS_MEMBRO = {"ativo", "nivelamento", "egresso"}
ETAPAS = {
    "revisao": "Revisão bibliográfica",
    "coleta": "Coleta",
    "tratamento": "Tratamento",
    "analise": "Análise",
    "escrita": "Escrita",
    "submissao": "Submissão",
    "publicada": "Publicada",
}
AREAS = {
    "dados": "Dados",
    "backend": "Back-end",
    "frontend": "Front-end",
    "fullstack": "Full Stack",
    "infra": "Infraestrutura",
}


def _load(nome):
    with open(DATA_DIR / f"{nome}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def _validar(membros, projetos, pesquisas):
    """Falha o build se houver id repetido, status inválido ou referência quebrada."""
    erros = []

    for nome, itens in (("membros", membros), ("projetos", projetos), ("pesquisas", pesquisas)):
        ids = [i["id"] for i in itens]
        repetidos = {i for i in ids if ids.count(i) > 1}
        if repetidos:
            erros.append(f"{nome}.yml: ids repetidos {sorted(repetidos)}")

    ids_membros = {m["id"] for m in membros}
    ids_projetos = {p["id"] for p in projetos}
    ids_pesquisas = {p["id"] for p in pesquisas}

    for m in membros:
        if m["status"] not in STATUS_MEMBRO:
            erros.append(f"membros.yml: '{m['id']}' com status inválido '{m['status']}'")
        if m.get("area") is not None and m["area"] not in AREAS:
            erros.append(f"membros.yml: '{m['id']}' com área inválida '{m['area']}'")
        for p in m.get("projetos") or []:
            if p not in ids_projetos:
                erros.append(f"membros.yml: '{m['id']}' cita projeto inexistente '{p}'")
        for p in m.get("pesquisas") or []:
            if p not in ids_pesquisas:
                erros.append(f"membros.yml: '{m['id']}' cita pesquisa inexistente '{p}'")

    for p in projetos:
        if p["status"] not in STATUS_PROJETO:
            erros.append(f"projetos.yml: '{p['id']}' com status inválido '{p['status']}'")
        if p.get("responsavel") and p["responsavel"] not in ids_membros:
            erros.append(f"projetos.yml: '{p['id']}' tem responsável inexistente '{p['responsavel']}'")

    for p in pesquisas:
        if p["status"] not in STATUS_PESQUISA:
            erros.append(f"pesquisas.yml: '{p['id']}' com status inválido '{p['status']}'")
        if p["etapa"] not in ETAPAS:
            erros.append(f"pesquisas.yml: '{p['id']}' com etapa inválida '{p['etapa']}'")
        for m in p.get("membros") or []:
            if m not in ids_membros:
                erros.append(f"pesquisas.yml: '{p['id']}' cita membro inexistente '{m}'")

    if erros:
        raise ValueError("Dados inválidos em data/:\n  - " + "\n  - ".join(erros))


def define_env(env):
    lab = _load("laboratorio")
    membros = _load("membros")
    projetos = _load("projetos")
    pesquisas = _load("pesquisas")
    _validar(membros, projetos, pesquisas)

    por_id = {
        **{("membro", m["id"]): m for m in membros},
        **{("projeto", p["id"]): p for p in projetos},
        **{("pesquisa", p["id"]): p for p in pesquisas},
    }

    env.variables.update({
        "lab": lab,
        "membros": membros,
        "projetos": projetos,
        "pesquisas": pesquisas,
        "contadores": {
            "membros_ativos": sum(m["status"] == "ativo" for m in membros),
            "em_nivelamento": sum(m["status"] == "nivelamento" for m in membros),
            "projetos_andamento": sum(p["status"] == "em-andamento" for p in projetos),
            "projetos_concluidos": sum(p["status"] == "concluido" for p in projetos),
            "projetos_planejados": sum(p["status"] == "planejado" for p in projetos),
            "pesquisas_total": len(pesquisas),
        },
    })

    @env.macro
    def nome(tipo, id_):
        """Nome de um membro, projeto ou pesquisa a partir do id."""
        item = por_id.get((tipo, id_))
        return item["nome"] if item else "—"

    @env.macro
    def nomes(tipo, ids):
        return ", ".join(nome(tipo, i) for i in ids) if ids else "—"

    @env.macro
    def status_projeto(s):
        return STATUS_PROJETO.get(s, s)

    @env.macro
    def status_pesquisa(s):
        return STATUS_PESQUISA.get(s, s)

    @env.macro
    def etapa(e):
        return ETAPAS.get(e, e)

    @env.macro
    def area(a):
        return AREAS.get(a, a) if a else "—"

    @env.macro
    def ou_traco(valor):
        if valor is None or valor == [] or valor == "":
            return "—"
        if isinstance(valor, list):
            return ", ".join(str(v) for v in valor)
        return valor


def on_post_build(env):
    """Exporta os dados em JSON para o site institucional: /api/<nome>.json"""
    destino = Path(env.conf["site_dir"]) / "api"
    destino.mkdir(parents=True, exist_ok=True)
    for nome in ("laboratorio", "membros", "projetos", "pesquisas"):
        (destino / f"{nome}.json").write_text(
            json.dumps(_load(nome), ensure_ascii=False, indent=2), encoding="utf-8"
        )
