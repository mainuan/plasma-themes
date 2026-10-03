# Dream color schemes

These KDE color schemes are maintained as Dream-compatible variants for KDE
Plasma 6 / Qt 6, targeting Kubuntu 26.04 LTS.

Upstream reference:
<https://github.com/L4ki/Dream-Plasma-Themes/tree/main/Dream%20Color%20Schemes>

The local set provides five complete Dark/Light families:

- `DreamBrownDarkColor.colors` / `DreamBrownLightColor.colors`
- `DreamGrayDarkColor.colors` / `DreamGrayLightColor.colors`
- `DreamCyanDarkColor.colors` / `DreamCyanLightColor.colors`
- `DreamLimeDarkColor.colors` / `DreamLimeLightColor.colors`
- `DreamMagentaDarkColor.colors` / `DreamMagentaLightColor.colors`

Display names are Portuguese: Marrom Escuro/Claro, Cinza Escuro/Claro,
Ciano Escuro/Claro, Lima Escuro/Claro and Magenta Escuro/Claro. Technical
ColorScheme identifiers and filenames remain unchanged.

## Palette rules

The neutral base remains close to the Dream style. Family identity is carried by
selection, focus, hover, active, link, visited, and window-decoration roles.
Dark variants use brighter accents for readability on dark backgrounds. Light
variants use darker accent text and slightly restrained focus/hover colors so
links and controls remain legible on light surfaces.

Negative, neutral, and positive foregrounds keep their semantic meaning instead
of being recolored to the theme accent.

### Lime interaction refinement

Lime keeps focus, active text and selection in the lime/olive family, with
turquoise/teal reserved for hover decorations and unselected links. Dark keeps
the original neutral surfaces; Light uses darker interaction colors.

| Role | Lime Dark (hex / RGB) | Lime Light (hex / RGB) |
| --- | --- | --- |
| Focus | `#CCF97D` / `204,249,125` | `#527000` / `82,112,0` |
| View hover decoration | `#50BEE0` / `80,190,224` | `#006F70` / `0,111,112` |
| Active text | `#D7FF6E` / `215,255,110` | `#486400` / `72,100,0` |
| Link | `#4CCADD` / `76,202,221` | `#00676A` / `0,103,106` |
| Selection fill | `#A7D248` / `167,210,72` | `#587600` / `88,118,0` |
| Selection alternate | `#C2EA66` / `194,234,102` | `#4B6500` / `75,101,0` |
| Selected text | `#172000` / `23,32,0` | `#F7FCEB` / `247,252,235` |

The repository's Dream `widgets/viewitem.svg` draws its hover center with
`ColorScheme-Highlight` at 20% opacity. In
[libplasma 6.6](https://github.com/KDE/libplasma/blob/Plasma/6.6/src/plasma/private/theme_p.cpp),
HighlightColor comes from Selection.BackgroundNormal. Consequently, changing
DecorationHover alone does not strengthen this launcher fill. Selection colors
deliberately increase its luminance difference from the surface. Dolphin's
unselected hover outline is refined separately through View.DecorationHover.

The visually approved Lime pair is the behavioral benchmark, not a source of
RGB values for other families. Its 20% Window blend is `#394233` at 1.56:1 Dark
and `#D1D8C1` at 1.29:1 Light. Brown/Gray/Cyan/Magenta now reach 1.47-1.51:1
Dark and 1.30-1.40:1 Light while retaining their own hues. Cyan Dark already had
a strong View hover, so only its selection was refined. Focus and neutral
surfaces are preserved. Selection text and semantic foregrounds change only to
remain legible after the brighter Dark / denser Light selection fills.

For all ten schemes, the validator models that 20% sRGB blend, checks ordinary
text on it, and enforces
minimum fill/surface contrast of 1.45:1 Dark and 1.25:1 Light. These are regression
thresholds for this translucent asset, not WCAG requirements or a substitute for
testing the actual launcher. Selected text is checked against both opaque
selection backgrounds independently.

## Validation

Run:

```sh
python3 tools/validate-color-schemes.py
git diff --check
python3 -m py_compile tools/validate-color-schemes.py
```

The validator checks required files, KConfig sections and keys, duplicate
schemes, RGB syntax and ranges, Dark/Light pair completeness, important
foreground/background contrast, family color identity, and legacy Lime scheme
identifiers, plus the expected Portuguese display names independently of
technical ColorScheme identifiers.

## Local Plasma test

Without installing a package system-wide, copy the schemes to the user data
directory:

```sh
mkdir -p ~/.local/share/color-schemes
cp usr/share/color-schemes/Dream*Color.colors ~/.local/share/color-schemes/
```

Then open System Settings > Colors & Themes > Colors and apply one scheme at a
time. This changes the active user session, so do it manually only when you want
to test the visual result.

For the final interaction retest, check Brown, Gray, Cyan and Magenta Dark/Light;
the Lime palettes are already visually approved. Choose the scheme's own accent rather than a custom
or wallpaper-derived accent. In the launcher, compare Internet, Graphics and
Office categories and application rows with the pointer and keyboard arrows;
also compare hover versus pressed items, search results and secondary text.
In Dolphin, check hover outlines, single/multiple selections and inactive
selections. Check links, buttons and text selection in KDE/Qt applications.
Repeat with the Dream Plasma Style and Breeze: a style's own colors or fixed SVG
opacities can affect the outcome. Restore the previous scheme/accent after the
test. No automatic test changes the active Plasma configuration.

If Plasma caches stale metadata, log out and back in first. When a real cache
refresh is required during manual testing, restart Plasma Shell from the user
session; avoid doing this from packaging or automated validation.

Some behavior can only be judged in a real Plasma session: Dolphin selection,
Kate text selection and links, Konsole contrast, menus, tooltips, inactive
windows, and any lock/logout screen components that consume the color scheme.
