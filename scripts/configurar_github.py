#!/usr/bin/env python3
"""
Configura o GitHub da organização a partir de data/github.yml:

  1. Cria (ou atualiza) as labels em todos os repositórios não arquivados.
  2. Cria o projeto "NARA — Roadmap", se ainda não existir.
  3. Cria os campos personalizados que ainda não existem no projeto.

Pode ser rodado várias vezes: o que já existe não é duplicado.

Pré-requisitos:
    gh auth login
    gh auth refresh -s project,read:org
    pip install pyyaml

Uso:
    python scripts/configurar_github.py              # aplica tudo
    python scripts/configurar_github.py --simular    # só mostra o que faria
    python scripts/configurar_github.py --so-labels
    python scripts/configurar_github.py --so-projeto
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"


def carregar(nome):
    with open(DATA / f"{nome}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def gh(*args, simular=False, json_saida=False):
    """Executa um comando do gh. Em modo simulação, comandos de escrita só são exibidos."""
    cmd = ["gh", *args]
    escrita = args[0] in ("label",) or args[:2] in (("project", "create"), ("project", "field-create"))
    if simular and escrita:
        print("  [simulação]", " ".join(cmd))
        return None
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Erro ao executar: {' '.join(cmd)}\n{r.stderr.strip()}")
    return json.loads(r.stdout) if json_saida else r.stdout


def aplicar_labels(cfg, simular):
    org = cfg["organizacao"]
    repos = gh("repo", "list", org, "--no-archived", "--limit", "200",
               "--json", "name", json_saida=True)
    print(f"\n== Labels em {len(repos)} repositórios ==")
    for repo in repos:
        alvo = f"{org}/{repo['name']}"
        print(f"- {alvo}")
        for lb in cfg["labels"]:
            gh("label", "create", lb["nome"], "--repo", alvo, "--color", lb["cor"],
               "--description", lb["descricao"], "--force", simular=simular)


def encontrar_ou_criar_projeto(cfg, simular):
    org, titulo = cfg["organizacao"], cfg["projeto"]
    dados = gh("project", "list", "--owner", org, "--format", "json",
               "--limit", "100", json_saida=True)
    for p in dados.get("projects", []):
        if p["title"] == titulo:
            print(f"\n== Projeto '{titulo}' já existe (nº {p['number']}) ==")
            return p["number"]

    print(f"\n== Criando projeto '{titulo}' ==")
    if simular:
        gh("project", "create", "--owner", org, "--title", titulo, simular=True)
        return None
    novo = json.loads(gh("project", "create", "--owner", org, "--title", titulo, "--format", "json"))
    print(f"  criado com nº {novo['number']}")
    return novo["number"]


def opcoes_projeto(cfg):
    nomes = [p["nome"] for p in carregar("projetos")]
    nomes += [f"Pesquisa: {p['nome']}" for p in carregar("pesquisas")]
    nomes += cfg.get("projetos_extras", [])
    # O CLI separa opções por vírgula, então vírgulas nos nomes viram " -"
    return [n.replace(",", " -") for n in nomes]


def aplicar_campos(cfg, numero, simular):
    org = cfg["organizacao"]
    existentes = set()
    if numero is not None:
        dados = gh("project", "field-list", str(numero), "--owner", org,
                   "--format", "json", "--limit", "100", json_saida=True)
        existentes = {f["name"] for f in dados.get("fields", [])}

    print("\n== Campos do projeto ==")
    for campo in cfg["campos"]:
        if campo["nome"] in existentes:
            print(f"- {campo['nome']}: já existe, mantido")
            continue
        args = ["project", "field-create", str(numero or "<novo>"), "--owner", org,
                "--name", campo["nome"], "--data-type", campo["tipo"]]
        if campo["tipo"] == "SINGLE_SELECT":
            opcoes = opcoes_projeto(cfg) if campo["opcoes"] == "automatico" else campo["opcoes"]
            args += ["--single-select-options", ",".join(opcoes)]
        print(f"- {campo['nome']}: criando")
        gh(*args, simular=simular or numero is None)


def main():
    ap = argparse.ArgumentParser(description="Configura labels e GitHub Projects do NARA")
    ap.add_argument("--simular", action="store_true", help="mostra as ações sem executar")
    grupo = ap.add_mutually_exclusive_group()
    grupo.add_argument("--so-labels", action="store_true")
    grupo.add_argument("--so-projeto", action="store_true")
    a = ap.parse_args()

    cfg = carregar("github")

    if not a.so_projeto:
        aplicar_labels(cfg, a.simular)
    if not a.so_labels:
        numero = encontrar_ou_criar_projeto(cfg, a.simular)
        aplicar_campos(cfg, numero, a.simular)
        if numero is not None:
            print(f"\nPronto. Projeto: https://github.com/orgs/{cfg['organizacao']}/projects/{numero}")
            print(f'Nos issue templates, use:  projects: ["{cfg["organizacao"]}/{numero}"]')

    print("\nFaltam os passos manuais: Status, Iteração e visões (veja Processo e rituais no handbook).")


if __name__ == "__main__":
    main()
