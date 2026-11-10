# Blackwall

A Cyberpunk theme picker for **Starship**, **Zed**, and **Ghostty**.
Choose an app, then choose an Edgerunners-inspired palette. Each app changes
independently.

Pure-black backgrounds, restrained Cyberpunk / Edgerunners accents, fine borders,
and Nerd Font icons. Built with Python 3 and an optional fzf picker.

| Theme | Character | Colors |
| --- | --- | --- |
| Overdrive | David | Yellow / mint |
| Moonwire | Lucy | Lavender / cyan |
| Riot | Rebecca | Mint / pink |
| Ghost | Adam Smasher | Red / silver |

## Requirements

- Python **3.9+**; no Python packages to install.
- [fzf](https://github.com/junegunn/fzf) for the interactive picker; a numbered
  menu is available without it.
- A Nerd Font, such as FiraCode Nerd Font, for the icons.
- The app you want to theme. Starship must already be enabled in your shell.

Designed and verified on macOS. The CLI uses the paths listed below; custom
`XDG_CONFIG_HOME` and `STARSHIP_CONFIG` locations are currently unsupported.

## Install

```sh
gh repo clone mesterM12/blackwall ~/Development/blackwall
cd ~/Development/blackwall
python3 scripts/install.py
blackwall
```

If you already cloned the repository, run the installer from that checkout.

The installer links `~/.local/bin/blackwall` directly to `bin/blackwall` in this
repository. Keep the checkout in place. If the command is not found, add
`export PATH="$HOME/.local/bin:$PATH"` to your shell configuration and open a
new terminal. The installer preserves an existing launcher in the backup folder.

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

## Settings and backups

| App | Settings | Installed theme assets |
| --- | --- | --- |
| Starship | `~/.config/starship.toml` | Preset is copied into its settings file |
| Zed | `~/.config/zed/settings.json` | `~/.config/zed/themes/blackwall.json` |
| Ghostty | `~/.config/ghostty/config` | `~/.config/ghostty/themes/Blackwall-<Theme>` |

Changed files are saved under
`~/.config/blackwall/backups/<timestamp>/`, keeping their paths relative to your
home folder. To restore a previous setting, copy that file back to its original
location and reload the app. For example, a Starship backup is stored as
`<timestamp>/.config/starship.toml`.

To update this checkout:

```sh
git pull --ff-only
```

The command already links to the source, so CLI updates take effect immediately.
Select a theme again to apply updated presets to an app.

To remove the command:

```sh
rm ~/.local/bin/blackwall
```

This removes the launcher link. Installed app settings and backups remain; restore
backed-up settings separately if desired.

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

GitHub Actions runs the isolated tests on Python 3.9 and 3.14 and checks that the
committed desktop presets match the palette generator.
