<div align="center">

<img src="https://raw.githubusercontent.com/mainuan/.github/main/profile/assets/mainuan-logo.svg" width="96" alt="Logotipo do Mainuan">

# Mainuan Plasma Themes

Temas, esquemas de cores, decorações de janela, cursores e widgets do KDE Plasma usados pelo **Mainuan Linux**, empacotados como `mainuan-plasma-themes`.

[![CI](https://github.com/mainuan/plasma-themes/actions/workflows/ci.yml/badge.svg)](https://github.com/mainuan/plasma-themes/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/mainuan/plasma-themes)](https://github.com/mainuan/plasma-themes/releases)
![Base](https://img.shields.io/badge/base-Kubuntu%2026.04%20LTS-0079c1)
![Plasma](https://img.shields.io/badge/KDE%20Plasma-6.6-1d99f3)

[English](README.en.md)

</div>

---

## O que é

Este repositório reúne os componentes visuais do Plasma 6 que o Mainuan usa ou
oferece: temas de terceiros (Dream e Blur-Glassy, de L4ki; MacTahoe e Lavanda,
de Vince Liuice), variações nas cores do Mainuan e widgets de vários autores.
A árvore `usr/share/` do repositório é instalada como está pelo pacote Debian
`mainuan-plasma-themes`.

O pacote vem instalado na ISO do Mainuan. A escolha do que fica ativo nas
novas contas (tema do Plasma `Dream-Color-Plasma`, esquema de cores
`DreamCyanLightColor`, decoração `Lavanda-Light`, widgets do painel) é feita
pelo [`mainuan-desktop-defaults`](https://github.com/mainuan/dot-files), não
por este pacote.

## O que o pacote contém

| Tipo | Itens | Onde o Plasma mostra |
|---|---|---|
| Temas globais (`look-and-feel`) | Dream Dark/Light, Blur-Glassy Dark/Light, MacTahoe Dark/Light | Cores e temas > Tema global |
| Temas do Plasma (`desktoptheme`) | `Dream-Color-Plasma`, `Blur-Glassy-Dark`, `Blur-Glassy-Light`, `MacTahoe-Dark`, `MacTahoe-Light` | Cores e temas > Tema do Plasma |
| Esquemas de cores | 12 Dream nas cores do Mainuan (Marrom, Cinza, Ciano, Lima, Magenta e Violeta, claro e escuro), 2 Blur-Glassy, 2 MacTahoe | Cores e temas > Cores |
| Decorações Aurorae | `Lavanda-Light` ("Mainuan-Claro"), `Lavanda-Dark` ("Mainuan-Escuro"), `MacTahoe-Light`, `MacTahoe-Dark` | Cores e temas > Decorações de janelas |
| Cursores | `cyan-cursor`, `brown-cursor`, `lavanda-cursor` (Bibata Modern) | Cores e temas > Cursores |
| Widgets (`plasmoids`) | Tahoe Launcher, KDE Control Station, Chaac Complete Weather, Deepin Menu Classic, Orbit Menu, Plasma Drawer, Overview, Compact Pager, KDE AI Chat | Adicionar widgets |

As regras de cor das famílias Dream estão em
[`docs/DREAM-COLOR-SCHEMES.md`](docs/DREAM-COLOR-SCHEMES.md).

## Instalação

O pacote já vem na ISO do Mainuan. Para instalar ou atualizar à mão, baixe o
`.deb` e o `SHA256SUMS` da
[última release](https://github.com/mainuan/plasma-themes/releases/latest):

```bash
sha256sum --check --ignore-missing SHA256SUMS
sudo apt install ./mainuan-plasma-themes_*_all.deb
```

O GitHub Releases não é um repositório APT: as atualizações chegam por novas
versões do pacote ou pela ISO.

## Convivência com o Plasma e o Kubuntu

Cada componente fica numa pasta ou arquivo de nome próprio em
`/usr/share/plasma`, `/usr/share/color-schemes`, `/usr/share/aurorae/themes` e
`/usr/share/icons`. Nenhum arquivo do Plasma ou do Kubuntu é substituído ou
desviado; o CI instala o pacote junto com o `plasma-workspace` para conferir.

Os leia-mes, as licenças e as fontes de tradução (`translate/`) dos widgets
ficam só no pacote-fonte; os créditos e licenças de cada componente estão no
[`debian/copyright`](debian/copyright).

## Adicionar ou atualizar um componente

1. Coloque o componente no caminho em que o Plasma o procura, dentro de
   `usr/share/` (por exemplo, `usr/share/plasma/plasmoids/<Id>/`). O nome da
   pasta de um widget ou tema global precisa ser igual ao `KPlugin.Id` do
   `metadata.json`, e o `metadata.json` precisa declarar `KPackageStructure`.
2. Registre autor, origem e licença numa entrada `Files:` do
   `debian/copyright`.
3. Se o teste de fumaça conta itens (16 esquemas de cores, 4 decorações,
   20 pacotes KPackage), atualize a contagem em `.github/workflows/ci.yml`.
4. Registre a mudança em `debian/changelog` (`dch -v <nova versão>`) e abra um
   pull request. A release é publicada quando a tag `v<versão>`, igual à de
   `debian/changelog`, é enviada.

## Informações técnicas

| Item | Valor |
|---|---|
| Pacote | `mainuan-plasma-themes` (`Architecture: all`) |
| Destino | `/usr/share/{plasma,color-schemes,aurorae,icons}` |
| Base | Kubuntu 26.04 LTS, KDE Plasma 6.6 |
| Empacotamento | debhelper 13, formato `3.0 (native)` |
| Recomenda | `plasma-workspace` |
| Dependências de build | `gettext`, `python3` (para os testes) |

## Compilação e testes

```bash
dpkg-buildpackage -us -uc -b
```

O [CI](.github/workflows/ci.yml) usa o pipeline compartilhado
[`mainuan/.github`](https://github.com/mainuan/.github) num contêiner
Ubuntu 26.04 e:

1. confere que o modelo de tradução está atualizado e que os catálogos são
   válidos (`po/i18n.sh check-pot` e `po/i18n.sh validate`);
2. valida os esquemas de cores Dream (`tools/validate-color-schemes.py`) e
   confere que os nomes traduzidos gravados nos `.colors` batem com `po/`
   (`po/apply-color-scheme-names.sh`);
3. confere que o pacote-fonte não leva `.git` nem sobras de build;
4. compila com `dpkg-buildpackage` e passa o `lintian` (falha em erro);
5. instala o pacote num Ubuntu 26.04 limpo, com o `plasma-workspace`, e
   confere cada widget, tema global e tema do Plasma (`metadata.json`,
   `main.qml`, `defaults`), os 16 esquemas de cores, os 3 cursores e as
   4 decorações; o `kpackagetool6` precisa listar os 20 pacotes;
6. reinstala, remove e expurga o pacote, sem sobras.

Uma tag `v<versão>` publica o `.deb` e o `SHA256SUMS` na release.

## Traduções

Os nomes dos 12 esquemas de cores Dream do Mainuan são traduzidos em
33 idiomas (`po/LINGUAS`). O `po/apply-color-scheme-names.sh` grava as
traduções como chaves `Name[<idioma>]` nos arquivos `.colors`; o português
do Brasil mantém os nomes originais (Ciano Claro, Marrom Escuro…). Os widgets
de terceiros trazem os próprios catálogos em `contents/locale`.

```bash
po/i18n.sh extract && po/i18n.sh update   # depois de mudar um nome
po/apply-color-scheme-names.sh            # grava as traduções nos .colors
```

## Contribuição

Relate problemas em [Issues](https://github.com/mainuan/plasma-themes/issues)
e envie mudanças por pull request. O CI roda em cada pull request, em
[Actions](https://github.com/mainuan/plasma-themes/actions).

## Créditos

**Mainuan** (pessoas com commits neste repositório):

- **Daigo** ([daigoasuka](https://github.com/daigoasuka)): seleção e
  adaptação dos temas, esquemas de cores e cursores.
- **Rafael Ruscher** ([ruscher](https://github.com/ruscher)): traduções,
  empacotamento Debian e CI.
- **Natanael Barbosa Santos** ([natanael-art](https://github.com/natanael-art)):
  decorações Lavanda nos temas globais.

**Projetos de origem** (conforme o `debian/copyright`):

| Componente | Autores | Origem | Licença |
|---|---|---|---|
| Blur-Glassy (temas globais, temas do Plasma, cores) | L4ki | [L4ki/Blur-Glassy](https://github.com/L4ki/Blur-Glassy) | GPL-3 |
| Dream (`Dream-Color-Plasma`, temas globais, cores) | L4ki; variações de cor do Mainuan | [L4ki/Dream-Plasma-Themes](https://github.com/L4ki/Dream-Plasma-Themes) | GPL-3+ (tema do Plasma), GPL-3 |
| MacTahoe (temas globais, temas do Plasma, Aurorae, cores) | Vince Liuice | [vinceliuice/MacTahoe-kde](https://github.com/vinceliuice/MacTahoe-kde) | GPL-3 |
| Lavanda (Aurorae "Mainuan-Claro/Escuro") | Vince Liuice | Lavanda KDE | GPL-3 |
| Cursores (Bibata Modern em cores do Mainuan) | Abdulkaiz Khatri | [ful1e5/Bibata_Cursor](https://github.com/ful1e5/Bibata_Cursor) | MIT (Expat) |
| Chaac Complete Weather | zayronxio (Adolfo) | [store.kde.org/p/2174265](https://store.kde.org/p/2174265/) | GPL-3+ |
| Compact Pager | Tino Lorenz, Diego Miguel | [tilorenz/compact_pager](https://github.com/tilorenz/compact_pager) | GPL-3+ |
| Overview | Himprakash Deka, com código do Plasma (Mikel Johnson, Ivan Čukić, Marco Martin, David Edmundson, Gregor Taetzner) | [himdek.com](https://himdek.com/Overview-Widget-for-Plasma/) | GPL-3+ |
| Deepin Menu Classic, Orbit Menu | zayronxio (Adolfo), com código do Plasma (Eike Hein, Aurélien Gâteau, Ivan Čukić) | [zayronxio/DeepinMenu.Classic](https://github.com/zayronxio/DeepinMenu.Classic), [store.kde.org/p/2228598](https://store.kde.org/p/2228598/) | GPL-2+ |
| KDE Control Station | Eliver Lara, com código do Plasma (Jan Grulich, Harald Sitter, Daniel Nicoletti, ivan tkachenko, Nate Graham, Sefa Eyeoglu, Marco Martin) | [EliverLara/kde-control-station](https://github.com/EliverLara/kde-control-station) | GPL-3 |
| KDE AI Chat | Rachit Asthana | [racstan/KDE-AI-Chat](https://github.com/racstan/KDE-AI-Chat) | GPL-2+ |
| Plasma Drawer | Connor Popp, com código do Plasma (Eike Hein, Aurélien Gâteau, Weng Xuetian) | [p-connor/plasma-drawer](https://github.com/p-connor/plasma-drawer) | GPL-2+ |
| Tahoe Launcher | Eliver Lara, Friedrich Schriewer, Prateek SU, com código do Plasma (Eike Hein, Aurélien Gâteau, Ivan Čukić, Weng Xuetian) | [EliverLara/TahoeLauncher](https://github.com/EliverLara/TahoeLauncher) | GPL-2+ |
| Ícones Feather (no Tahoe Launcher) | Cole Bemis | [feathericons.com](https://feathericons.com/) | MIT (Expat) |
| Ícones Lucide (no Tahoe Launcher) | Lucide Contributors | [lucide.dev](https://lucide.dev/) | ISC |

## Licença

O trabalho original do Mainuan neste repositório (traduções em `po/`,
`tools/`, documentação e empacotamento) é distribuído sob a **GNU General
Public License versão 2** (GPL-2.0), texto em [`LICENSE`](LICENSE).

Os temas, cursores e widgets de terceiros mantêm a licença dos seus autores
(tabela de créditos acima e [`debian/copyright`](debian/copyright)). As
adaptações do Mainuan feitas sobre temas GPL-3 continuam sob a GPL-3, porque
uma obra derivada de GPL-3 não pode ser relicenciada como GPL-2.
