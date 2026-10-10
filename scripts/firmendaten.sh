#!/usr/bin/env bash
# Kompatibilitäts-Hülle – die eigentliche Arbeit macht scripts/firmendaten.py.
#   bash scripts/firmendaten.sh               Vorschau-Build nach dist/
#   bash scripts/firmendaten.sh --produktion  Produktions-Build, bricht bei offenen Angaben ab
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/firmendaten.py "$@"
