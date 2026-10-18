#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m compileall -q gas_station_mis
python -m unittest discover -s gas_station_mis/tests -p "test_*.py" -v
if command -v node >/dev/null 2>&1; then
  find gas_station_mis/gas_station_mis -name '*.js' -print0 | xargs -0 -r -n1 node --check
fi
