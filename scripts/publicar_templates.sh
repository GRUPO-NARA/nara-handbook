#!/usr/bin/env bash
# Publica os issue templates e o template de PR no repositório GRUPO-NARA/.github.
#
# Os arquivos de origem ficam em templates-organizacao/.github/ neste repositório.
# Para mudar um template: edite aqui, faça o commit no handbook e rode este script.
#
# Uso (de dentro da pasta do nara-handbook):
#   bash scripts/publicar_templates.sh

set -euo pipefail

ORG="GRUPO-NARA"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ORIGEM="$RAIZ/templates-organizacao/.github"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Baixando $ORG/.github..."
gh repo clone "$ORG/.github" "$TMP/repo" -- --depth 1 --quiet

echo "→ Copiando templates..."
mkdir -p "$TMP/repo/.github"
rm -rf "$TMP/repo/.github/ISSUE_TEMPLATE"
cp -r "$ORIGEM/." "$TMP/repo/.github/"

cd "$TMP/repo"
git add .github

if git diff --cached --quiet; then
  echo "✓ Nada mudou: os templates já estão atualizados."
  exit 0
fi

echo "→ Arquivos alterados:"
git diff --cached --name-status | sed 's/^/   /'

git commit --quiet -m "feat: atualiza issue templates e template de PR da organização"
git push --quiet
echo "✓ Templates publicados em https://github.com/$ORG/.github"
