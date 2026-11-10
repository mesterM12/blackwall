"""Behavior checks in isolated homes; never write real app settings."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'bin/blackwall'
MODULE = runpy.run_path(str(CLI), run_name='blackwall_test')


class BlackwallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='blackwall-test-')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.env = dict(os.environ, HOME=str(self.home))
        self.fixtures = {
            '.config/starship.toml': '# original\n',
            '.config/ghostty/config': '# keep\nfont-size = 15\ntheme = Old\n',
            '.config/zed/settings.json': '{\n  // keep this comment\n  "theme": {"dark":"Old", "light":"Other", "mode":"dark"},\n  "font": 15,\n}\n',
            '.pi/agent/settings.json': '{"theme":"keep"}\n',
        }
        for path, text in self.fixtures.items():
            target = self.home / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *args], env=self.env, capture_output=True, text=True)

    def test_each_app_changes_independently_with_bundled_themes(self):
        for app, alias, path in [('starship', 'lucy', '.config/starship.toml'),
                                 ('zed', 'rebecca', '.config/zed/settings.json'),
                                 ('ghostty', 'smasher', '.config/ghostty/config')]:
            before = {p: (self.home / p).read_bytes() for p in self.fixtures}
            result = self.run_cli(app, alias)
            self.assertEqual(result.returncode, 0, result.stderr)
            changed = {p for p, value in before.items() if (self.home / p).read_bytes() != value}
            self.assertEqual(changed, {path})
            self.assertEqual(json.loads((self.home / '.pi/agent/settings.json').read_text())['theme'], 'keep')
        zed = (self.home / '.config/zed/settings.json').read_text()
        parsed = MODULE['jsonc'](zed)[0]
        self.assertIn('// keep this comment', zed)
        self.assertEqual(parsed['theme']['light'], 'Other')
        self.assertEqual(parsed['font'], 15)
        self.assertIn('font-size = 15', (self.home / '.config/ghostty/config').read_text())
        self.assertTrue(list((self.home / '.config/blackwall/backups').rglob('starship.toml')))

    def test_zed_comments_trailing_commas_and_string_contents_survive(self):
        cases = ['{}\n', '{\n  "font": "value,}", // keep\n}\n',
                 '{\n  "font": 15 // keep\n}\n', '{\n  "font": 15,\n  // last comment\n}\n']
        for text in cases:
            with self.subTest(text=text):
                updated = MODULE['set_zed_theme'](text, 'Blackwall Moonwire')
                parsed = MODULE['jsonc'](updated)[0]
                self.assertEqual(parsed['theme'], 'Blackwall Moonwire')
                if '// keep' in text:
                    self.assertIn('// keep', updated)
                if 'value,}' in text:
                    self.assertEqual(parsed['font'], 'value,}')

    def test_invalid_settings_or_theme_leave_app_files_untouched(self):
        path = self.home / '.config/zed/settings.json'
        path.write_text('{invalid settings')
        before = {p: (self.home / p).read_bytes() for p in self.fixtures}
        for args in [('zed', 'lucy'), ('starship', 'invalid')]:
            self.assertNotEqual(self.run_cli(*args).returncode, 0)
            self.assertEqual({p: (self.home / p).read_bytes() for p in self.fixtures}, before)

    def test_installer_links_to_this_repo_and_keeps_the_link_on_repeat(self):
        target = self.home / '.local/bin/blackwall'
        target.parent.mkdir(parents=True)
        target.write_text('# old launcher\n')
        for _ in range(2):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/install.py')], env=self.env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), CLI)
        result = subprocess.run([str(target), 'status'], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Starship', result.stdout)
        backups = list((self.home / '.config/blackwall/backups').rglob('blackwall-launcher'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), '# old launcher\n')


if __name__ == '__main__':
    unittest.main()
