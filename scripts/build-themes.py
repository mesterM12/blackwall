"""Build desktop themes from the four bundled Blackwall palettes. Does not install."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'themes'
(out/'ghostty').mkdir(exist_ok=True)
(out/'zed').mkdir(exist_ok=True)
(out/'starship').mkdir(exist_ok=True)
family = {'$schema':'https://zed.dev/schema/themes/v0.2.0.json', 'name':'Blackwall', 'author':'pi-choom', 'themes':[]}
characters = {'blackwall-overdrive':'Overdrive','blackwall-moonwire':'Moonwire','blackwall-riot':'Riot','blackwall-ghost':'Ghost'}
for ident, character in characters.items():
    pi = json.loads((root/f'themes/{ident}.json').read_text())
    v = pi['vars']
    def color(token):
        value = pi['colors'].get(token, token)
        while value in v: value = v[value]
        return value
    def brighten(value):
        return '#' + ''.join(f'{round(int(value[i:i+2],16)*.75+255*.25):02x}' for i in (1,3,5))
    accent, focus, text = v['accent'], v['focus'], v['text']
    ansi = ['#000000',v['red'],v['green'],v['yellow'],v['blue'],color('syntaxKeyword'),color('syntaxFunction'),text,
            v['dim'],brighten(v['red']),brighten(v['green']),brighten(v['yellow']),brighten(v['blue']),brighten(color('syntaxKeyword')),brighten(color('syntaxFunction')),'#f5f7f6']
    ghostty = [f'# Blackwall {character} — generated from themes/{ident}.json',
               'background = #000000',f'foreground = {text}',f'cursor-color = {accent}',
               'cursor-text = #000000',f'selection-background = {v["selection"]}',
               f'selection-foreground = {text}']
    ghostty += [f'palette = {i}={c}' for i,c in enumerate(ansi)]
    (out/f'ghostty/Blackwall-{character}').write_text('\n'.join(ghostty)+'\n')
    style = {}
    for key in ['background','elevated_surface.background','surface.background','element.background','element.disabled',
                'status_bar.background','title_bar.background','title_bar.inactive_background','toolbar.background',
                'tab_bar.background','tab.inactive_background','tab.active_background','panel.background','scrollbar.track.background',
                'editor.background','editor.gutter.background','editor.subheader.background','editor.active_line.background',
                'editor.highlighted_line.background','terminal.background']:
        style[key] = '#000000'
    for key in ['element.hover','element.active','element.selected','drop_target.background','ghost_element.hover',
                'ghost_element.active','ghost_element.selected','editor.document_highlight.read_background','editor.document_highlight.write_background']:
        style[key] = '#222222'
    style.update({'ghost_element.background':'#000000','ghost_element.disabled':'#000000',
        'border':v['borderMuted'],'border.variant':v['borderMuted'],'border.focused':focus,'border.selected':accent,
        'border.transparent':'#00000000','border.disabled':'#222222',
        'text':text,'text.muted':v['muted'],'text.placeholder':v['dim'],'text.disabled':'#888888','text.accent':accent,
        'icon':v['muted'],'icon.muted':v['dim'],'icon.disabled':'#888888','icon.placeholder':v['dim'],'icon.accent':accent,
        'search.match_background':'#292929','search.active_match_background':'#383838',
        'panel.focused_border':focus,'pane.focused_border':focus,'pane_group.border':v['borderMuted'],
        'scrollbar.thumb.background':v['borderMuted'],'scrollbar.thumb.hover_background':v['border'],
        'scrollbar.thumb.border':'#000000','scrollbar.track.border':'#000000',
        'editor.foreground':text,'editor.line_number':'#888888','editor.active_line_number':accent,'editor.hover_line_number':focus,
        'editor.invisible':'#404040','editor.wrap_guide':'#222222','editor.active_wrap_guide':v['borderMuted'],
        'editor.indent_guide':'#222222','editor.indent_guide_active':v['border'],
        'terminal.foreground':text,'terminal.bright_foreground':'#ffffff','terminal.dim_foreground':v['dim'],
        'link_text.hover':focus})
    for i,key in enumerate(['black','red','green','yellow','blue','magenta','cyan','white']):
        style[f'terminal.ansi.{key}'] = ansi[i]
        style[f'terminal.ansi.bright_{key}'] = ansi[i+8]
        style[f'terminal.ansi.dim_{key}'] = ansi[i]
    for key,c in {'conflict':v['yellow'],'created':v['green'],'deleted':v['red'],'error':v['red'],
                  'hidden':v['dim'],'hint':v['dim'],'ignored':v['dim'],'info':focus,'modified':v['yellow'],
                  'predictive':v['dim'],'renamed':focus,'success':v['green'],'unreachable':v['dim'],'warning':v['yellow']}.items():
        style[key] = c
        style[f'{key}.background'] = '#000000'
        style[f'{key}.border'] = c
    for key,c in {'added':v['green'],'modified':v['yellow'],'deleted':v['red']}.items():
        style[f'version_control.{key}'] = c
    style['version_control.word_added'] = '#193523'
    style['version_control.word_deleted'] = '#402023'
    style['players'] = [{'cursor':accent,'background':accent,'selection':'#222222'}]
    syntax = {}
    groups = {
        'text':['variable','variable.special','property','parameter','punctuation','punctuation.bracket','punctuation.delimiter','punctuation.special','operator','identifier','embedded'],
        'syntaxKeyword':['keyword','keyword.control','boolean','tag','preproc'],
        'syntaxFunction':['function','function.method','constructor'],
        'syntaxString':['string','string.regex','string.special','string.special.symbol','text.literal'],
        'syntaxType':['type','type.builtin','enum','variant'],
        'syntaxNumber':['number','constant','string.escape'],
        'syntaxComment':['comment','comment.doc'],
        'accent':['title','label','attribute','link_text'],
        'borderAccent':['link_uri'],
    }
    for token, names in groups.items():
        for name in names: syntax[name] = {'color':color(token),'font_style':'normal','font_weight':400}
    syntax['emphasis'] = {'color':text,'font_style':'italic','font_weight':400}
    syntax['emphasis.strong'] = {'color':text,'font_style':'normal','font_weight':700}
    style['syntax'] = syntax
    # Shell prompt shares the rail vocabulary without painting large color blocks.
    shell = [
        '# Blackwall ' + character + ' — generated from the Pi palette',
        '"$schema" = "https://starship.rs/config-schema.json"',
        'command_timeout = 2000',
        'add_newline = true',
        'palette = "blackwall"',
        'format = """',
        '[╭─ 󰆍 ' + character.upper() + '](bold accent) $os$username$hostname$fill$time',
        '[│](rail)$directory$git_branch$git_status',
        '[╰─](rail)$c$rust$golang$nodejs$php$java$kotlin$haskell$python$docker_context$conda$status$jobs$cmd_duration$character"""',
        'continuation_prompt = "[│ ](rail)[… ](focus)"',
        '',
        '[fill]', 'symbol = "─"', 'style = "rail"',
        '[os]', 'disabled = false', 'format = "[$symbol ](muted)"',
        '[os.symbols]', 'Macos = "󰀵"', 'Linux = "󰌽"', 'Windows = ""',
        '[username]', 'show_always = true', 'style_user = "muted"',
        'style_root = "bold red"', 'format = "[$user ]($style)"',
        '[hostname]', 'ssh_only = true', 'format = "[@$hostname ](focus)"',
        '[directory]', 'style = "bold focus"', 'format = "[  $path]($style)[$read_only](red) "',
        'read_only = " "', 'truncation_length = 2', 'truncation_symbol = "…/"',
        'truncate_to_repo = true',
        '[git_branch]', 'symbol = " "', 'style = "muted"',
        'format = "[$symbol$branch(:$remote_branch) ]($style)"',
        'truncation_length = 18', 'truncation_symbol = "…"',
        '[git_status]', 'style = "yellow"', 'format = "([$all_status$ahead_behind]($style) )"',
        'conflicted = "!$count "', 'stashed = "≡$count "', 'deleted = "−$count "',
        'renamed = "»$count "', 'modified = "~$count "', 'staged = "+$count "', 'untracked = "?$count "',
        'ahead = "⇡$count "', 'behind = "⇣$count "', 'diverged = "⇡$ahead_count⇣$behind_count "',
        '[time]', 'disabled = false', 'time_format = "%R"',
        'style = "dim"', 'format = "[  $time]($style)"',
        '[status]', 'disabled = false', 'style = "red"',
        'symbol = " "', 'format = "[ $symbol$status]($style) "',
        'pipestatus = true', 'pipestatus_format = "[ $pipestatus]($style) "',
        '[jobs]', 'symbol = " "', 'style = "focus"',
        'number_threshold = 1', 'symbol_threshold = 1', 'format = "[ $symbol$number]($style) "',
        '[cmd_duration]', 'min_time = 2000', 'show_milliseconds = true',
        'style = "dim"', 'format = "[ 󱎫 $duration]($style) "',
        'show_notifications = true', 'min_time_to_notify = 45000',
        '[character]', 'success_symbol = "[ ❯](bold accent)"',
        'error_symbol = "[ ❯](bold red)"', 'vimcmd_symbol = "[ ❮](bold focus)"',
        'vimcmd_replace_one_symbol = "[ R](bold red)"',
        'vimcmd_replace_symbol = "[ R](bold red)"', 'vimcmd_visual_symbol = "[ V](bold yellow)"',
    ]
    for module, symbol in {'c':'','rust':'','golang':'','nodejs':'','php':'','java':'','kotlin':'','haskell':'','python':''}.items():
        shell += ['', '['+module+']', 'symbol = "'+symbol+' "', 'style = "muted"',
                  r"format = '[ $symbol($version)( \($virtualenv\))]($style) " + "'" if module == 'python' else 'format = "[ $symbol($version)]($style) "']
    shell += ['', '[docker_context]', 'symbol = " "', 'style = "muted"',
              'format = "[ $symbol$context]($style) "',
              '[conda]', 'symbol = " "', 'style = "muted"',
              'format = "[ $symbol$environment]($style) "', 'ignore_base = false',
              '', '[palettes.blackwall]']
    for key in ['accent','focus','text','muted','dim','red','green','yellow']:
        shell.append(f'{key} = "{v[key]}"')
    shell.append(f'rail = "{v["borderMuted"]}"')
    (out/f'starship/{ident}.toml').write_text('\n'.join(shell)+'\n')
    family['themes'].append({'name':f'Blackwall {character}','appearance':'dark','style':style})
(out/'zed/blackwall.json').write_text(json.dumps(family,indent=2)+'\n')
print('Built four Ghostty themes, four Starship prompts and a four-mode Zed family from bundled source palettes.')
