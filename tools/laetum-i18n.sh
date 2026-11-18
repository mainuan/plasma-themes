#!/bin/sh
# Translations of the Laetum Control Center widget (local.laetum.controlcenter).
#
#   tools/laetum-i18n.sh pot      regenerate translate/template.pot from the QML
#   tools/laetum-i18n.sh merge    merge template.pot into every translate/*.po
#   tools/laetum-i18n.sh compile  build contents/locale/*/LC_MESSAGES/*.mo
#   tools/laetum-i18n.sh check    validate the catalogs and that the .mo files
#                                 match them (used by the CI)
#
# Plasma loads the catalog "plasma_applet_<Id>" from the widget's
# contents/locale directory.
set -eu
cd "$(dirname "$0")/../usr/share/plasma/plasmoids/local.laetum.controlcenter"
domain=plasma_applet_local.laetum.controlcenter

case "${1:-}" in
    pot)
        find contents \( -name '*.qml' -o -name '*.js' \) | sort > translate/.files
        xgettext --from-code=UTF-8 -L JavaScript --kde -ci18n -ki18n:1 -ki18nc:1c,2 \
            -ki18np:1,2 -ki18ncp:1c,2,3 --package-name=local.laetum.controlcenter \
            --msgid-bugs-address=https://github.com/PcmciaKai/Laetum-Control-Center/issues \
            --files-from=translate/.files -o translate/template.pot
        rm -f translate/.files
        ;;
    merge)
        for po in translate/*.po; do
            msgmerge --quiet --update --backup=none "$po" translate/template.pot
        done
        ;;
    compile)
        rm -rf contents/locale
        for po in translate/*.po; do
            lang=$(basename "$po" .po)
            mkdir -p "contents/locale/$lang/LC_MESSAGES"
            msgfmt --check -o "contents/locale/$lang/LC_MESSAGES/$domain.mo" "$po"
        done
        ;;
    check)
        tmp=$(mktemp -d)
        trap 'rm -rf "$tmp"' EXIT
        n=0
        for po in translate/*.po; do
            lang=$(basename "$po" .po)
            msgfmt --check --statistics -o "$tmp/$lang.mo" "$po"
            mo="contents/locale/$lang/LC_MESSAGES/$domain.mo"
            [ -f "$mo" ] || { echo "missing $mo (run: tools/laetum-i18n.sh compile)" >&2; exit 1; }
            msgunfmt "$mo" > "$tmp/committed.po"
            msgunfmt "$tmp/$lang.mo" > "$tmp/fresh.po"
            cmp -s "$tmp/committed.po" "$tmp/fresh.po" \
                || { echo "$mo is out of date (run: tools/laetum-i18n.sh compile)" >&2; exit 1; }
            # Every message of the template is translated.
            if msgattrib --untranslated --no-obsolete "$po" | grep -q '^msgid "[^"]'; then
                echo "$po has untranslated messages" >&2; exit 1
            fi
            n=$((n + 1))
        done
        echo "$n catalogs ok"
        ;;
    *)
        sed -n '2,11p' "$0"; exit 2 ;;
esac
