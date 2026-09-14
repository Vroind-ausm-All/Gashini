#!/usr/bin/env bash
# Setzt die Werte aus data/firmendaten.env in alle Vorlagen ein
# und legt den fertigen Auftritt im Ordner dist/ ab.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENVFILE="$ROOT/data/firmendaten.env"
DIST="$ROOT/dist"

[ -f "$ENVFILE" ] || { echo "Fehlt: $ENVFILE"; exit 1; }
# shellcheck disable=SC1090
set -a; . "$ENVFILE"; set +a

rm -rf "$DIST"
mkdir -p "$DIST"
cp -r "$ROOT/web" "$ROOT/print" "$ROOT/brand" "$DIST/"

KEYS=$(grep -oE '^[A-Z0-9_]+=' "$ENVFILE" | tr -d '=')

offen=0
while IFS= read -r -d '' datei; do
  for k in $KEYS; do
    wert="${!k-}"
    # Sonderzeichen für sed maskieren
    wert_esc=$(printf '%s' "$wert" | sed -e 's/[&|\\]/\\&/g')
    sed -i "s|{{$k}}|$wert_esc|g" "$datei"
  done
done < <(find "$DIST" -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.xml' -o -name '*.txt' -o -name '*.md' \) -print0)

echo "Fertig: $DIST"
if grep -rlq '{{[A-Z0-9_]*}}' "$DIST"; then
  echo
  echo "ACHTUNG – folgende Platzhalter sind noch offen:"
  grep -rhoE '\{\{[A-Z0-9_]+\}\}' "$DIST" | sort -u
  offen=1
fi
exit $offen
