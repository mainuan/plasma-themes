<div align="center">

<img src="https://raw.githubusercontent.com/mainuan/.github/main/profile/assets/mainuan-logo.svg" width="96" alt="Mainuan logo">

# Mainuan Plasma Themes

KDE Plasma themes, colour schemes, window decorations, cursors and widgets used by **Mainuan Linux**, packaged as `mainuan-plasma-themes`.

[![CI](https://github.com/mainuan/plasma-themes/actions/workflows/ci.yml/badge.svg)](https://github.com/mainuan/plasma-themes/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/mainuan/plasma-themes)](https://github.com/mainuan/plasma-themes/releases)

[Português](README.md)

</div>

---

## What it is

The `usr/share/` tree of this repository is installed as-is by the
`mainuan-plasma-themes` package, which ships with the Mainuan ISO:

- global themes: Dream, Blur-Glassy and MacTahoe (dark and light);
- Plasma styles: `Dream-Color-Plasma`, Blur-Glassy and MacTahoe;
- 16 colour schemes, including 12 Dream schemes in the Mainuan accent colours;
- Aurorae decorations: Lavanda ("Mainuan-Claro/Escuro") and MacTahoe;
- Bibata Modern cursors in cyan, brown and lavender;
- widgets: Tahoe Launcher, KDE Control Station, Chaac Complete Weather,
  Deepin Menu Classic, Orbit Menu, Plasma Drawer, Overview, Compact Pager and
  KDE AI Chat.

Everything lives under its own name; no Plasma or Kubuntu file is replaced or
diverted. Which theme, colour scheme and widgets are active on new accounts is
decided by [`mainuan-desktop-defaults`](https://github.com/mainuan/dot-files).

## Installation

Download the `.deb` and `SHA256SUMS` from the
[latest release](https://github.com/mainuan/plasma-themes/releases/latest):

```bash
sha256sum --check --ignore-missing SHA256SUMS
sudo apt install ./mainuan-plasma-themes_*_all.deb
```

## Build and tests

```bash
dpkg-buildpackage -us -uc -b
```

The [CI](.github/workflows/ci.yml) checks the translation template and
catalogs, validates the Dream colour schemes, builds the package in
Ubuntu 26.04, runs `lintian`, installs it next to `plasma-workspace`, checks
every widget, global theme, Plasma style, colour scheme, cursor and
decoration (`kpackagetool6` must list all 20 KPackages), then reinstalls,
removes and purges it. A `v<version>` tag publishes the `.deb` and
`SHA256SUMS`.

The names of the 12 Mainuan Dream colour schemes are translated into
33 languages from `po/`.

## Credits and license

Mainuan contributors: Daigo ([daigoasuka](https://github.com/daigoasuka)),
Rafael Ruscher ([ruscher](https://github.com/ruscher)) and Natanael Barbosa
Santos ([natanael-art](https://github.com/natanael-art)).

Third-party work, as recorded in [`debian/copyright`](debian/copyright):
Blur-Glassy and Dream by L4ki; MacTahoe and Lavanda by Vince Liuice; Bibata
cursors by Abdulkaiz Khatri; widgets by zayronxio, Tino Lorenz and Diego
Miguel, Himprakash Deka, Eliver Lara, Rachit Asthana, Connor Popp, Friedrich
Schriewer and Prateek SU, with code from KDE Plasma authors; Feather icons by
Cole Bemis and Lucide icons by the Lucide contributors. The Portuguese README
lists each component with its source and license.

Mainuan's original work in this repository (translations in `po/`, `tools/`,
documentation and packaging) is distributed under the **GNU General Public
License version 2** (GPL-2.0), see [`LICENSE`](LICENSE). Each third-party
component keeps its author's license (GPL-2+, GPL-3, GPL-3+, MIT or ISC).
Mainuan's adaptations of GPL-3 themes remain under the GPL-3, since a work
derived from GPL-3 code cannot be relicensed as GPL-2.
