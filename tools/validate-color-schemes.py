#!/usr/bin/env python3
"""Validate the Dream color schemes maintained by this repository."""

from __future__ import annotations

import math
import re
import sys
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEME_DIR = ROOT / "usr" / "share" / "color-schemes"

FAMILIES = ("Brown", "Gray", "Cyan", "Lime", "Magenta")
MODES = ("Dark", "Light")
TARGETS = [f"Dream{family}{mode}Color.colors" for family in FAMILIES for mode in MODES]
DISPLAY_NAMES = {
    "DreamBrownDarkColor": "Marrom Escuro",
    "DreamBrownLightColor": "Marrom Claro",
    "DreamGrayDarkColor": "Cinza Escuro",
    "DreamGrayLightColor": "Cinza Claro",
    "DreamCyanDarkColor": "Ciano Escuro",
    "DreamCyanLightColor": "Ciano Claro",
    "DreamLimeDarkColor": "Lima Escuro",
    "DreamLimeLightColor": "Lima Claro",
    "DreamMagentaDarkColor": "Magenta Escuro",
    "DreamMagentaLightColor": "Magenta Claro",
}

BASE_SECTIONS = (
    "ColorEffects:Disabled",
    "ColorEffects:Inactive",
    "Colors:Button",
    "Colors:Complementary",
    "Colors:Header",
    "Colors:Selection",
    "Colors:Tooltip",
    "Colors:View",
    "Colors:Window",
    "General",
    "KDE",
    "WM",
)

COLOR_KEYS = (
    "BackgroundAlternate",
    "BackgroundNormal",
    "DecorationFocus",
    "DecorationHover",
    "ForegroundActive",
    "ForegroundInactive",
    "ForegroundLink",
    "ForegroundNegative",
    "ForegroundNeutral",
    "ForegroundNormal",
    "ForegroundPositive",
    "ForegroundVisited",
)

RGB_RE = re.compile(r"^\d{1,3},\d{1,3},\d{1,3}$")


def expected_keys(filename: str) -> dict[str, tuple[str, ...]]:
    dark = "Dark" in filename
    header_key = "ForegroundVisited" if dark else "ForegroundInactive"
    return {
        "ColorEffects:Disabled": (
            "Color",
            "ColorAmount",
            "ColorEffect",
            "ContrastAmount",
            "ContrastEffect",
            "IntensityAmount",
            "IntensityEffect",
        ),
        "ColorEffects:Inactive": (
            "ChangeSelectionColor",
            "Color",
            "ColorAmount",
            "ColorEffect",
            "ContrastAmount",
            "ContrastEffect",
            "Enable",
            "IntensityAmount",
            "IntensityEffect",
        ),
        "Colors:Button": COLOR_KEYS,
        "Colors:Complementary": COLOR_KEYS,
        "Colors:Header": (header_key,),
        "Colors:Selection": COLOR_KEYS,
        "Colors:Tooltip": COLOR_KEYS,
        "Colors:View": COLOR_KEYS,
        "Colors:Window": COLOR_KEYS,
        "General": ("ColorScheme", "Name", "shadeSortColumn"),
        "KDE": ("contrast",),
        "WM": (
            "activeBackground",
            "activeBlend",
            "activeForeground",
            "inactiveBackground",
            "inactiveBlend",
            "inactiveForeground",
        ),
    }


def parse(path: Path) -> tuple[OrderedDict[str, OrderedDict[str, str]], list[str]]:
    data: OrderedDict[str, OrderedDict[str, str]] = OrderedDict()
    problems: list[str] = []
    current: str | None = None
    seen_sections: set[str] = set()

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") or line.endswith("]"):
            if not (line.startswith("[") and line.endswith("]") and line.count("[") == 1 and line.count("]") == 1):
                problems.append(f"{path}: line {lineno}: ERROR: malformed section header: {raw}")
                current = None
                continue
            current = line[1:-1]
            if current in seen_sections:
                problems.append(f"{path}: line {lineno}: ERROR: duplicate section [{current}]")
            seen_sections.add(current)
            data.setdefault(current, OrderedDict())
            continue
        if "=" not in raw:
            problems.append(f"{path}: line {lineno}: ERROR: malformed line without key=value: {raw}")
            continue
        if current is None:
            problems.append(f"{path}: line {lineno}: ERROR: key outside any section: {raw}")
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            problems.append(f"{path}: line {lineno}: ERROR: empty key")
            continue
        if key in data[current]:
            problems.append(f"{path}: line {lineno}: ERROR: duplicate key [{current}] {key}")
        data[current][key] = value
    return data, problems


def is_rgb_key(section: str, key: str) -> bool:
    return (
        key in COLOR_KEYS
        or key == "Color"
        or (section == "WM" and key.lower().endswith(("background", "blend", "foreground")))
    )


def parse_rgb(value: str) -> tuple[int, int, int] | None:
    if not RGB_RE.match(value):
        return None
    parts = tuple(int(part) for part in value.split(","))
    if any(part < 0 or part > 255 for part in parts):
        return None
    return parts  # type: ignore[return-value]


def luminance(rgb: tuple[int, int, int]) -> float:
    vals = []
    for channel in rgb:
        c = channel / 255
        vals.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la = luminance(a)
    lb = luminance(b)
    light, dark = max(la, lb), min(la, lb)
    return (light + 0.05) / (dark + 0.05)


def rgb_at(data: OrderedDict[str, OrderedDict[str, str]], section: str, key: str) -> tuple[int, int, int]:
    value = data[section][key]
    parsed = parse_rgb(value)
    if parsed is None:
        raise ValueError(f"invalid RGB at [{section}] {key}: {value}")
    return parsed


def validate_identity(path: Path, data: OrderedDict[str, OrderedDict[str, str]]) -> list[str]:
    problems: list[str] = []
    family = next(family for family in FAMILIES if family in path.name)
    roles = (
        ("Colors:Button", "DecorationFocus"),
        ("Colors:Button", "DecorationHover"),
        ("Colors:Button", "ForegroundLink"),
        ("Colors:Complementary", "ForegroundActive"),
        ("Colors:Selection", "BackgroundNormal"),
        ("Colors:View", "ForegroundLink"),
        ("Colors:Window", "ForegroundLink"),
        ("Colors:View", "DecorationFocus"),
        ("Colors:View", "DecorationHover"),
        ("Colors:Selection", "BackgroundAlternate"),
    )
    if family == "Lime":
        roles = tuple(
            (section, key)
            for section in ("Colors:Button", "Colors:Complementary", "Colors:Tooltip", "Colors:View", "Colors:Window")
            for key in ("DecorationFocus", "DecorationHover", "ForegroundActive", "ForegroundLink")
        ) + (("Colors:Selection", "BackgroundNormal"), ("Colors:Selection", "BackgroundAlternate"))

    def bad(rgb: tuple[int, int, int], key: str) -> bool:
        r, g, b = rgb
        if family == "Brown":
            return not (r > g > b and r - b >= 45)
        if family == "Gray":
            return max(rgb) - min(rgb) > 35
        if family == "Cyan":
            return not (b >= g >= r and b - r >= 70 and g - r >= 55)
        if family == "Lime":
            lime = g > r > b and g - b >= 90 and r - b >= 45
            # Teal/turquoise supports hover and links; focus, active and selection stay lime.
            support = (
                key in ("DecorationHover", "ForegroundLink")
                and r <= g * 0.45
                and g - r >= 55 and b - r >= 55
                and 0.85 * g <= b <= 1.35 * g
            )
            return not (lime or support)
        if family == "Magenta":
            return not (r > b > g and r - g >= 75 and b - g >= 55)
        return False

    for section, key in roles:
        color = rgb_at(data, section, key)
        if bad(color, key):
            problems.append(f"{path}: [{section}] {key}: ERROR: color {color} does not match {family} identity")
    return problems


def validate_interaction(path: Path, data: OrderedDict[str, OrderedDict[str, str]]) -> list[str]:
    problems: list[str] = []
    selection = rgb_at(data, "Colors:Selection", "BackgroundNormal")
    dark = "Dark" in path.name
    minimum_hover = 1.45 if dark else 1.25
    # Visually approved Lime anchors these regression floors; they are not WCAG rules.
    # Dream viewitem.svg tints hover-center with Selection.BackgroundNormal at 20% opacity.
    for section in ("Colors:Window", "Colors:View", "Colors:Button", "Colors:Complementary"):
        background = rgb_at(data, section, "BackgroundNormal")
        ratio = contrast(selection, background)
        if ratio < 3.0:
            problems.append(
                f"{path}: [Colors:Selection] BackgroundNormal: ERROR: contrast {ratio:.2f}:1 against [{section}] BackgroundNormal below 3.0:1"
            )
        hover = tuple(round(0.2 * s + 0.8 * b) for s, b in zip(selection, background))
        ratio = contrast(hover, background)
        if ratio < minimum_hover:
            problems.append(
                f"{path}: [Colors:Selection] BackgroundNormal: ERROR: Dream 20% hover contrast {ratio:.2f}:1 against [{section}] BackgroundNormal below {minimum_hover:.2f}:1"
            )
        foreground = rgb_at(data, section, "ForegroundNormal")
        ratio = contrast(foreground, hover)
        if ratio < 4.5:
            problems.append(
                f"{path}: [{section}] ForegroundNormal: ERROR: text contrast {ratio:.2f}:1 on Dream 20% hover below 4.5:1"
            )

    alternate = rgb_at(data, "Colors:Selection", "BackgroundAlternate")
    for key, minimum in (("ForegroundNormal", 4.5), ("ForegroundLink", 4.5), ("ForegroundActive", 3.0), ("ForegroundInactive", 3.0), ("ForegroundVisited", 3.0)):
        ratio = contrast(rgb_at(data, "Colors:Selection", key), alternate)
        if ratio < minimum:
            problems.append(
                f"{path}: [Colors:Selection] {key}: ERROR: contrast {ratio:.2f}:1 against BackgroundAlternate below {minimum:.1f}:1"
            )
    for key in ("ForegroundNegative", "ForegroundNeutral", "ForegroundPositive"):
        foreground = rgb_at(data, "Colors:Selection", key)
        for background_key in ("BackgroundNormal", "BackgroundAlternate"):
            ratio = contrast(foreground, rgb_at(data, "Colors:Selection", background_key))
            if ratio < 3.0:
                problems.append(
                    f"{path}: [Colors:Selection] {key}: ERROR: semantic contrast {ratio:.2f}:1 against {background_key} below 3.0:1"
                )
    return problems


def validate_file(path: Path, colorschemes: dict[str, Path]) -> list[str]:
    data, problems = parse(path)
    expected = expected_keys(path.name)

    for section in BASE_SECTIONS:
        if section not in data:
            problems.append(f"{path}: [{section}]: ERROR: missing required section")
            continue
        missing = set(expected[section]) - set(data[section])
        extra = set(data[section]) - set(expected[section])
        for key in sorted(missing):
            problems.append(f"{path}: [{section}] {key}: ERROR: missing required key")
        for key in sorted(extra):
            problems.append(f"{path}: [{section}] {key}: ERROR: unexpected key")

    if problems:
        return problems

    expected_scheme = path.stem
    scheme = data["General"]["ColorScheme"]
    if scheme != expected_scheme:
        problems.append(f"{path}: [General] ColorScheme: ERROR: expected {expected_scheme}, got {scheme}")
    if scheme in colorschemes:
        problems.append(f"{path}: [General] ColorScheme: ERROR: duplicate ColorScheme also in {colorschemes[scheme]}")
    colorschemes[scheme] = path

    expected_name = DISPLAY_NAMES[path.stem]
    if data["General"]["Name"] != expected_name:
        problems.append(f"{path}: [General] Name: ERROR: expected {expected_name}, got {data['General']['Name']}")
    if data["General"]["shadeSortColumn"] != "true":
        problems.append(f"{path}: [General] shadeSortColumn: ERROR: expected true")

    for section, keys in data.items():
        for key, value in keys.items():
            if not is_rgb_key(section, key):
                continue
            parsed = parse_rgb(value)
            if parsed is None:
                problems.append(f"{path}: [{section}] {key}: ERROR: invalid RGB value {value!r}; expected R,G,B in 0..255")

    if problems:
        return problems

    text_pairs = (
        ("ForegroundNormal", 4.5),
        ("ForegroundLink", 4.5),
        ("ForegroundActive", 3.0),
        ("ForegroundInactive", 3.0),
    )
    for section in ("Colors:Window", "Colors:View", "Colors:Button", "Colors:Tooltip", "Colors:Complementary", "Colors:Selection"):
        bg = rgb_at(data, section, "BackgroundNormal")
        for fg_key, minimum in text_pairs:
            fg = rgb_at(data, section, fg_key)
            if fg == bg:
                problems.append(f"{path}: [{section}] {fg_key}: ERROR: foreground equals BackgroundNormal")
                continue
            ratio = contrast(fg, bg)
            if ratio < minimum:
                problems.append(
                    f"{path}: [{section}] {fg_key}: ERROR: contrast {ratio:.2f}:1 against BackgroundNormal below {minimum:.1f}:1"
                )
        if section != "Colors:Selection":
            for deco_key in ("DecorationFocus", "DecorationHover"):
                deco = rgb_at(data, section, deco_key)
                ratio = contrast(deco, bg)
                if ratio < 3.0:
                    problems.append(
                        f"{path}: [{section}] {deco_key}: ERROR: contrast {ratio:.2f}:1 against BackgroundNormal below 3.0:1"
                    )

    semantic_keys = ("ForegroundNegative", "ForegroundNeutral", "ForegroundPositive")
    for section in ("Colors:Window", "Colors:View", "Colors:Button", "Colors:Tooltip", "Colors:Complementary", "Colors:Selection"):
        values = {key: rgb_at(data, section, key) for key in semantic_keys}
        if len(set(values.values())) != len(values):
            problems.append(f"{path}: [{section}]: ERROR: semantic foreground colors must remain distinct")

    problems.extend(validate_identity(path, data))
    problems.extend(validate_interaction(path, data))
    return problems


def validate_pairs(parsed: dict[str, OrderedDict[str, OrderedDict[str, str]]]) -> list[str]:
    problems: list[str] = []
    for family in FAMILIES:
        dark = f"Dream{family}DarkColor.colors"
        light = f"Dream{family}LightColor.colors"
        if dark not in parsed or light not in parsed:
            problems.append(f"{SCHEME_DIR}: {family}: ERROR: incomplete Dark/Light pair")

    for mode in MODES:
        names = [f"Dream{family}{mode}Color.colors" for family in FAMILIES if f"Dream{family}{mode}Color.colors" in parsed]
        if not names:
            continue
        reference = names[0]
        reference_shape = {
            section: tuple(parsed[reference][section].keys())
            for section in parsed[reference]
        }
        for name in names[1:]:
            shape = {section: tuple(parsed[name][section].keys()) for section in parsed[name]}
            if shape != reference_shape:
                problems.append(f"{SCHEME_DIR / name}: ERROR: unexpected structural difference from {reference}")
    return problems


def validate_legacy_lime() -> list[str]:
    problems: list[str] = []
    if (SCHEME_DIR / "Lima-Dark.colors").exists():
        problems.append(f"{SCHEME_DIR / 'Lima-Dark.colors'}: ERROR: legacy Lime color-scheme file must not exist")

    legacy_patterns = ("ColorScheme=LimaDark", "ColorScheme=LimaLight", "DreamLimeGreenDarkColor", "DreamLimeGreenLightColor")
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in legacy_patterns:
            if pattern in text:
                problems.append(f"{path}: ERROR: legacy Lime identifier remains: {pattern}")
    return problems


def main() -> int:
    problems: list[str] = []
    colorschemes: dict[str, Path] = {}
    parsed: dict[str, OrderedDict[str, OrderedDict[str, str]]] = {}

    for filename in TARGETS:
        path = SCHEME_DIR / filename
        if not path.exists():
            problems.append(f"{path}: ERROR: missing target scheme file")
            continue
        file_problems = validate_file(path, colorschemes)
        problems.extend(file_problems)
        data, _ = parse(path)
        parsed[filename] = data

    problems.extend(validate_pairs(parsed))
    problems.extend(validate_legacy_lime())

    if problems:
        for problem in problems:
            print(problem)
        print(f"\nValidation failed: {len(problems)} problem(s).")
        return 1

    print(f"Validated {len(TARGETS)} Dream color schemes successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
