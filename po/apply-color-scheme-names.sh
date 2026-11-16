#!/usr/bin/env bash
# Write the translated display names (Name[<lang>]=…) into the Mainuan color
# schemes from po/*.po. The .colors files are installed as-is (the ISO copies
# this repository), so the translations live in the files themselves, exactly
# like KDE's own color schemes. Idempotent; run after updating translations.
set -euo pipefail
cd "$(dirname "$0")/.."
for f in usr/share/color-schemes/Dream*.colors; do
  tmp=$(mktemp)
  # drop previous translations, then let msgfmt merge the current ones
  grep -v '^Name\[' "$f" > "$tmp.src"
  msgfmt --desktop --keyword=Name --template="$tmp.src" -d po -o "$tmp"
  if ! cmp -s "$tmp" "$f"; then cp "$tmp" "$f"; echo "updated $f"; fi
  rm -f "$tmp" "$tmp.src"
done
