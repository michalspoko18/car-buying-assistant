#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="car-buying-assistant"
PYTHON_VERSION="3.11"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="${REPO_ROOT}/car_buying_assistant"

if ! command -v conda >/dev/null 2>&1; then
  echo "[error] Nie znaleziono polecenia 'conda'. Zainstaluj Anacondę/Minicondę i spróbuj ponownie." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"

if ! conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
  echo "[info] Tworzę środowisko conda: ${ENV_NAME} (Python ${PYTHON_VERSION})"
  conda create -y -n "${ENV_NAME}" "python=${PYTHON_VERSION}"
fi

echo "[info] Aktywuję środowisko conda: ${ENV_NAME}"
conda activate "${ENV_NAME}"

echo "[info] Instaluję zależności Python"
python -m pip install --upgrade pip
python -m pip install -r "${REPO_ROOT}/requirements.txt"

if [ ! -f "${PROJECT_DIR}/.env" ]; then
  echo "[info] Tworzę plik .env z env.example"
  cp "${REPO_ROOT}/env.example" "${PROJECT_DIR}/.env"
  echo "[info] Uzupełnij OPENAI_API_KEY w ${PROJECT_DIR}/.env"
fi

echo "[info] Wykonuję migracje bazy danych"
cd "${PROJECT_DIR}"
python manage.py migrate

echo "[info] Gotowe. Uruchom aplikację:"
echo "  cd ${PROJECT_DIR} && python manage.py runserver 0.0.0.0:8000"
