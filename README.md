# Blackwall

A small theme picker for **Starship**, **Zed**, and **Ghostty**. Choose an app,
then choose a character palette. Each app changes independently.

Pure-black backgrounds, restrained Cyberpunk / Edgerunners accents, fine borders,
and Nerd Font icons. Built with Python 3 and an optional fzf picker.

| Theme | Character | Colors |
| --- | --- | --- |
| Overdrive | David | Yellow / mint |
| Moonwire | Lucy | Lavender / cyan |
| Riot | Rebecca | Mint / pink |
| Ghost | Adam Smasher | Red / silver |

## Install

Keep this repository at `~/Development/blackwall`, then run:

```sh
python3 scripts/install.py
```

The installer links `~/.local/bin/blackwall` directly to `bin/blackwall` in this
repository. Put `~/.local/bin` on your PATH. Python 3.9+ is required; install
[fzf](https://github.com/junegunn/fzf) for the arrow-key picker. Without it, the CLI
uses a numbered menu. A Nerd Font, such as FiraCode Nerd Font, renders the icons.

## Use

```sh
blackwall               # choose app, then theme
blackwall zed           # go straight to Zed's theme picker
blackwall ghostty lucy  # select Moonwire for Ghostty
blackwall status        # show each app's selection
```

Use arrow keys and Enter in the picker; Escape cancels. Theme names are
`overdrive`, `moonwire`, `riot`, and `ghost`. Character aliases `david`, `lucy`,
`rebecca`, `smasher`, and `adam` also work.

Starship updates at the next prompt. Zed watches its settings. In Ghostty on
macOS, press **Cmd+Shift+,** to reload its configuration.

The tool updates the selected app under `~/.config/` and backs up changed files
under `~/.config/blackwall/backups/`. Other apps and Pi keep their themes. Zed
comments, trailing commas, and unrelated preferences are preserved. Starship
selection replaces its prompt config with the bundled character preset.

## Develop

The CLI and every required theme are contained in this repository. It has no
runtime dependency on pi-choom, Codex folders, or the original checkout.

- `bin/blackwall`: CLI, app selection, config updates and backups.
- `themes/blackwall-*.json`: source palettes, originally developed alongside Pi.
- `themes/{starship,zed,ghostty}/`: generated desktop presets.
- `scripts/build-themes.py`: rebuild desktop presets from source palettes.
- `scripts/install.py`: link the command to this checkout.

```sh
python3 scripts/build-themes.py
python3 -m unittest discover -s tests
```

Rebuilding does not change app settings. Run `blackwall` to apply an updated
preset. Tests use temporary home folders and do not touch your real settings.
