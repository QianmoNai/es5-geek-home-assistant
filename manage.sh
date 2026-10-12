#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
venv_dir="${ESPHOME_VENV:-/tmp/es5-geek-venv}"
if [[ ! -x "$venv_dir/bin/esphome" ]]; then
  python3 -m venv "$venv_dir"
  "$venv_dir/bin/pip" install 'esphome==2026.9.1'
fi
command_name="${1:-compile}"
if [[ $# -gt 0 ]]; then shift; fi
exec "$venv_dir/bin/esphome" "$command_name" "$project_dir/geek.yaml" "$@"
