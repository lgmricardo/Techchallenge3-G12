#!/usr/bin/env bash
# Cria/atualiza o venv local (.venv) e instala requirements.txt.
# PySpark 3.5.1 exige JDK 8, 11 ou 17 — JDK 21+ remove o Security Manager que o Spark 3.5 usa
# internamente e a sessão falha ao subir. Este script só avisa sobre a versão do Java; não a instala.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d ".venv" ]; then
  echo "Criando .venv..."
  "$PYTHON_BIN" -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "Dependências instaladas em .venv/"

if command -v java >/dev/null 2>&1; then
  JAVA_VERSION="$(java -version 2>&1 | head -1)"
  echo "Java detectado: $JAVA_VERSION"
  MAJOR="$(java -version 2>&1 | head -1 | sed -E 's/.*"([0-9]+)\..*/\1/; s/.*"([0-9]+)"/\1/')"
  if [[ "$MAJOR" =~ ^[0-9]+$ ]] && [ "$MAJOR" -ne 17 ] && [ "$MAJOR" -ne 11 ] && [ "$MAJOR" -ne 8 ]; then
    echo "AVISO: PySpark 3.5.1 exige JDK 8, 11 ou 17. Instale um deles (ex.: 'brew install openjdk@17')"
    echo "e aponte JAVA_HOME para ele antes de rodar os jobs/notebooks."
  fi
else
  echo "AVISO: nenhum 'java' encontrado no PATH. PySpark 3.5.1 exige JDK 8, 11 ou 17 instalado"
  echo "e JAVA_HOME apontando para ele (ex.: 'brew install openjdk@17')."
fi

echo "Pronto. Ative o ambiente com: source .venv/bin/activate"
