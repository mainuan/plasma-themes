#!/usr/bin/python3 -I
"""Regression gate: the Laetum Control Center opens without the grey header.

In Mainuan the popup starts on the Controls / Notifications tabs. The opaque
band with the System Settings and Power buttons is opt-in (showHeader), and a
drill-in page keeps its Back row. Run from the repository root.
"""
import re
import sys
import xml.etree.ElementTree as ET

BASE = "usr/share/plasma/plasmoids/local.laetum.controlcenter/contents/"
errors = []


def need(cond, msg):
    if not cond:
        errors.append(msg)


# 1. The option exists and is off by default
ns = {"k": "http://www.kde.org/standards/kcfg/1.0"}
entries = {e.get("name"): e for e in ET.parse(BASE + "config/main.xml").getroot().iter("{%s}entry" % ns["k"])}
need("showHeader" in entries, "main.xml: no showHeader entry")
if "showHeader" in entries:
    d = entries["showHeader"].find("k:default", ns)
    need(entries["showHeader"].get("type") == "Bool", "main.xml: showHeader is not Bool")
    need(d is not None and d.text.strip() == "false", "main.xml: showHeader must default to false")

panel = open(BASE + "ui/Panel.qml", encoding="utf-8").read()
config = open(BASE + "ui/ConfigGeneral.qml", encoding="utf-8").read()


def block(text, ident):
    """The body of the QML object with the given id (brace matched)."""
    m = re.search(r"\bid:\s*%s\b" % ident, text)
    if not m:
        return ""
    start = text.rfind("{", 0, m.start())
    depth, i = 0, start
    while i < len(text):
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return text[start:i + 1]
        i += 1
    return ""


# 2. The panel reads the option
need(re.search(r"property bool showHeader:\s*Plasmoid\.configuration\.showHeader", panel),
     "Panel.qml: showHeader is not bound to the configuration")

# 3. The header row only shows with the option or on a page
header = block(panel, "header")
need(re.search(r"visible:\s*panel\.showHeader\s*\|\|\s*panel\.pageOpen", header),
     "Panel.qml: the header is not hidden on the home view")
need(re.search(r"ShadowedRectangle\s*\{\s*visible:\s*panel\.showHeader", header),
     "Panel.qml: the grey band is drawn without showHeader")

# 4. System Settings and Power live only in the home header, which needs the option
home = block(panel, "homeHeader")
need("configure-symbolic" in home and "system-shutdown-symbolic" in home,
     "Panel.qml: the System Settings / Power buttons moved out of homeHeader")
need(re.search(r"visible:\s*panel\.showHeader\s*&&\s*!panel\.pageOpen", home),
     "Panel.qml: homeHeader is visible without showHeader")
outside = panel.replace(home, "")
need("configure-symbolic" not in outside and "system-shutdown-symbolic" not in outside,
     "Panel.qml: a System Settings / Power button outside the optional header")

# 5. A page keeps its Back row
page = block(panel, "pageHeader")
need("go-previous-symbolic" in page and "panel.closePage()" in page,
     "Panel.qml: drill-in pages lost their Back button")

# 6. Users can turn it back on
need("cfg_showHeader: showHeaderCheck.checked" in config, "ConfigGeneral.qml: no showHeader checkbox")

if errors:
    for e in errors:
        print("::error::" + e)
    sys.exit(1)
print("Laetum Control Center: header off by default, Back row kept on pages")
