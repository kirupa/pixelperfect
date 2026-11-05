"""Checks that the pixel-emoji skill is complete, portable and working.

Run from the repository root:

    python -m unittest discover -s tests -v

The sprite checks need Pillow and numpy (pip install -r skills/pixel-emoji/scripts/requirements.txt); nothing
here downloads anything. To test an installed copy of the skill instead of this repository's, set
PIXEL_EMOJI_SKILL_DIR to its folder; the repository-only checks (README, CI) are then skipped.
"""
import ast
import contextlib
import hashlib
import io
import json
import os
import re
import shlex
import site
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True   # importing the tool must not leave __pycache__ in the skill folder

ROOT = Path(__file__).resolve().parent.parent
REPO_SKILL = (ROOT / "skills" / "pixel-emoji").resolve()
SKILL = Path(os.environ.get("PIXEL_EMOJI_SKILL_DIR") or REPO_SKILL).expanduser().resolve()
IN_REPO = SKILL == REPO_SKILL
TOOL = SKILL / "scripts" / "sprite_tool.py"
SCAN_ROOT = ROOT if IN_REPO else SKILL
BINARY = {".png", ".gif", ".jpg", ".jpeg", ".zip", ".pyc", ".ttf", ".ttc", ".otf"}

# Machine- and project-specific strings that must never appear (split so this file doesn't contain them).
FORBIDDEN = ["/" + "Users/", "C:" + "\\Users", "session" + "-state", "copilot" + "-worktrees",
             "kirupa-crispy" + "-spoon", "Drop" + "box", "need" + "_repo"]
HOST_PATHS = ["tools/" + "pixel_twemoji", "icon/" + "pixel-twemoji"]   # allowed only in a host's *-pipeline.md

FRONTMATTER_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
IN_SKILL_PREFIXES = ("scripts/", "references/", "templates/", "examples/", "assets/", "skills/pixel-emoji/",
                     "docs/", "tests/", ".github/workflows/")
EXTERNAL_PATHS = ("assets/svg",)   # Twemoji's own layout, inside its zips and on its CDN
TYPED = {"N": "2", "SEED": "7", "SIZE": "16", "AXIS": "15", "COMMAND": "check"}


def text_files(root=SCAN_ROOT):
    for path in sorted(root.rglob("*")):
        parts = path.relative_to(root).parts
        if ".git" in parts or "__pycache__" in parts or not path.is_file() or path.suffix.lower() in BINARY:
            continue
        yield path


def markdown_files():
    return [p for p in text_files() if p.suffix.lower() == ".md"]


def read(path):
    return path.read_text(encoding="utf-8")


FENCE = re.compile(r"^(\s*)(```|~~~)[^\n]*\n(.*?)^\1\2[ \t]*$", re.S | re.M)
INLINE = re.compile(r"(`+)(.+?)\1", re.S)


def code_blocks(text):
    return [m.group(3) for m in FENCE.finditer(text)]


def prose(text):
    """TEXT without fenced blocks or inline code."""
    return INLINE.sub(" ", FENCE.sub("\n", text))


def inline_code(text):
    return [m.group(2).strip() for m in INLINE.finditer(FENCE.sub("\n", text))]


def frontmatter(text):
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with a '---' frontmatter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("SKILL.md's frontmatter has no closing '---' line")
    return text[4:end + 1]


PLAIN_BAD_START = tuple("[]{}&*!|>'\"%@`,?:-#")
YAML_SPECIAL = re.compile(r"(?i)^(true|false|yes|no|on|off|null|~|[-+]?(\d[\d_]*)?(\.\d*)?([eE][-+]?\d+)?|\.inf|\.nan)$")


def scalar(value, where):
    """One YAML scalar from the small subset SKILL.md uses: plain, or double- or single-quoted."""
    if value[:1] == '"':
        if not value.endswith('"') or len(value) < 2:
            raise AssertionError(f"{where}: unterminated double-quoted value")
        return json.loads(value)
    if value[:1] == "'":
        if not value.endswith("'") or len(value) < 2:
            raise AssertionError(f"{where}: unterminated single-quoted value")
        return value[1:-1].replace("''", "'")
    if value.startswith(PLAIN_BAD_START) or ": " in value or " #" in value or value.endswith(":"):
        raise AssertionError(f"{where}: quote this value; plain YAML can't hold it: {value[:60]!r}")
    if YAML_SPECIAL.match(value):
        raise AssertionError(f"{where}: {value!r} would load as a number, bool or null; quote it")
    return value


def parse_frontmatter(block):
    data, parent = {}, None
    for number, line in enumerate(block.splitlines(), 2):
        where = f"SKILL.md:{number}"
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            if parent is None or "\t" in line[:len(line) - len(line.lstrip())]:
                raise AssertionError(f"{where}: unexpected indentation")
            key, sep, value = line.strip().partition(":")
            if not sep or not value.startswith(" ") or not value.strip():
                raise AssertionError(f"{where}: nested lines are 'key: value'")
            data[parent][key] = scalar(value.strip(), where)
            continue
        key, sep, value = line.partition(":")
        if not sep or not re.fullmatch(r"[a-z][a-z-]*", key):
            raise AssertionError(f"{where}: top-level lines are 'key: value'")
        if key in data:
            raise AssertionError(f"{where}: {key} is set twice")
        if not value.strip():
            data[key], parent = {}, key
        else:
            if not value.startswith(" "):
                raise AssertionError(f"{where}: put a space after '{key}:'")
            data[key], parent = scalar(value.strip(), where), None
    return data


def tool():
    """The skill's sprite_tool module, imported in-process."""
    if "sprite_tool" not in sys.modules:
        sys.path.insert(0, str(TOOL.parent))
        try:
            import sprite_tool   # noqa: F401
        finally:
            sys.path.remove(str(TOOL.parent))
    return sys.modules["sprite_tool"]


def clean_env(scratch):
    """An environment with a throwaway home, cache and work folder, and no downloads."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("PIXEL_EMOJI_")}
    home = Path(scratch) / "home"
    for sub in ("", "cache", "work", "AppData/Local", ".cache"):
        (home / sub).mkdir(parents=True, exist_ok=True)
    env.update({
        "HOME": str(home), "USERPROFILE": str(home), "LOCALAPPDATA": str(home / "AppData" / "Local"),
        "XDG_CACHE_HOME": str(home / ".cache"), "PIXEL_EMOJI_CACHE": str(home / "cache"),
        "PIXEL_EMOJI_WORK": str(home / "work"), "PIXEL_EMOJI_OFFLINE": "1",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8",
    })
    if "PYTHONUSERBASE" not in env:
        env["PYTHONUSERBASE"] = site.getuserbase()   # a new HOME must not hide packages installed with --user
    return env


def run_tool(args, env, cwd=SKILL):
    return subprocess.run([sys.executable, str(TOOL)] + list(args), cwd=str(cwd), env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=900)


def documented_commands():
    """(file, line text, arguments) for every sprite_tool command shown in the docs."""
    found = []
    for md in markdown_files():
        text = read(md)
        lines = [ln for block in code_blocks(text) for ln in block.splitlines()] + inline_code(text)
        for line in lines:
            if "sprite_tool.py" not in line:
                continue
            line = line.strip()
            for prompt in ("$ ", "> ", "PS> "):
                if line.startswith(prompt):
                    line = line[len(prompt):]
            if not re.match(r"(python3?|py)(\.exe)?\s", line) or line.startswith("python3 -m"):
                continue
            found.append((md, line))
    return found


def command_args(line):
    tokens = shlex.split(line.replace("\\", "/"), comments=True)
    at = next(i for i, t in enumerate(tokens) if t.endswith("sprite_tool.py"))
    args = []
    for token in tokens[at + 1:]:
        token = token.strip("[]")
        for dots in ("...", "\u2026"):
            token = token[:-len(dots)] if token.endswith(dots) else token
        if token:
            args.append(TYPED.get(token, token))
    return tokens[:at + 1], args


class Frontmatter(unittest.TestCase):
    """SKILL.md follows the Agent Skills specification (https://agentskills.io/specification)."""

    def setUp(self):
        self.text = read(SKILL / "SKILL.md")
        self.block = frontmatter(self.text)
        self.data = parse_frontmatter(self.block)

    def test_fields(self):
        data = self.data
        self.assertLessEqual(set(data), FRONTMATTER_KEYS, "only the specification's fields")
        self.assertEqual(data.get("name"), SKILL.name, "name must equal the skill's folder name")
        self.assertRegex(data["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(data["name"]), 64)
        self.assertTrue(1 <= len(data.get("description", "")) <= 1024, "description: 1-1024 characters")
        if "compatibility" in data:
            self.assertTrue(1 <= len(data["compatibility"]) <= 500, "compatibility: 1-500 characters")
        if "metadata" in data:
            self.assertIsInstance(data["metadata"], dict)
            for key, value in data["metadata"].items():
                self.assertIsInstance(value, str, f"metadata.{key} must be a string")
        if "license" in data:
            self.assertIsInstance(data["license"], str)

    def test_yaml_agrees(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML isn't installed; the stdlib parser checked the subset")
        self.assertEqual(yaml.safe_load(self.block), self.data)

    def test_short_enough(self):
        self.assertLessEqual(len(self.text.splitlines()), 500, "keep SKILL.md under 500 lines")


class Links(unittest.TestCase):
    """Every relative link and every cited in-skill path resolves, and the skill never links outside itself."""

    def test_markdown_links(self):
        link = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
        ref = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", re.M)
        html = re.compile(r"""\b(?:src|href)\s*=\s*["']([^"']+)["']""")
        bad = []
        for md in markdown_files():
            text = prose(read(md))
            targets = link.findall(text) + ref.findall(text) + html.findall(text)
            for target in targets:
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                path = unquote(target.split("#", 1)[0].split("?", 1)[0])
                resolved = (md.parent / path).resolve()
                if not resolved.exists():
                    bad.append(f"{md.relative_to(SCAN_ROOT)}: {target} doesn't exist")
                elif SKILL in md.parents and SKILL not in resolved.parents and resolved != SKILL:
                    bad.append(f"{md.relative_to(SCAN_ROOT)}: {target} leaves the skill folder")
        self.assertEqual(bad, [])

    def test_cited_paths(self):
        bad, checked = [], 0
        for md in markdown_files() + [p for p in text_files() if p.suffix in (".sprite", ".py")]:
            text = read(md)
            spans = inline_code(text) + code_blocks(text) if md.suffix == ".md" else [text]
            for span in spans:
                for token in re.split(r"[\s\"'(),;=|]+", span):
                    token = token.rstrip(".:")
                    if token.startswith("./"):
                        token = token[2:]
                    if not token.startswith(IN_SKILL_PREFIXES) or token.startswith(EXTERNAL_PATHS):
                        continue
                    if re.search(r"[<>*{}$%\u2026]|\.\.\.", token):
                        continue
                    token = re.sub(r"(\.py):.*$", r"\1", token.split("@", 1)[0])
                    segments = [s for s in token.split("/") if s]
                    if any(re.fullmatch(r"[A-Z][A-Z0-9_]*", s) for s in segments):
                        continue   # a placeholder such as DIR or NAME
                    bases = [md.parent, SKILL, ROOT if IN_REPO else SKILL]
                    if not any((base / token).exists() for base in bases):
                        bad.append(f"{md.relative_to(SCAN_ROOT)}: {token}")
                    checked += 1
        self.assertGreater(checked, 50, "the docs cite their files by path")
        self.assertEqual(sorted(set(bad)), [])


class Portability(unittest.TestCase):
    """Nothing points at one machine, one project or a private session."""

    def test_forbidden_strings(self):
        bad = []
        for path in text_files():
            text = read(path)
            if not IN_REPO and path == SKILL / "SKILL.md":
                # gh skill install --from-local records the folder it copied from; that line is the installer's
                text = re.sub(r"(?m)^[ \t]+local-path:.*$", "", text)
            words = FORBIDDEN + ([] if path.name.endswith("-pipeline.md") else HOST_PATHS)
            for word in words:
                if word in text:
                    line = text[:text.index(word)].count("\n") + 1
                    bad.append(f"{path.relative_to(SCAN_ROOT)}:{line}: {word}")
        self.assertEqual(bad, [])

    def test_python_39_syntax(self):
        for path in text_files():
            if path.suffix == ".py":
                ast.parse(read(path), filename=str(path), feature_version=(3, 9))

    def test_tool_is_self_contained(self):
        source = read(TOOL)
        imports = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                imports |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                imports.add(node.module.split(".")[0])
        stdlib = set(getattr(sys, "stdlib_module_names", ())) or None
        optional = {"PIL", "numpy", "resvg_py", "fontTools"}
        if stdlib:
            self.assertEqual(sorted(imports - stdlib - optional), [], "only the stdlib, Pillow, numpy and extras")
        self.assertNotRegex(source, r"(?m)^\s*(?:from|import)\s+(?:tools|pixel_twemoji)")

    def test_documented_commands_parse(self):
        parser = tool().build_parser()
        commands = documented_commands()
        self.assertGreater(len(commands), 40)
        bad = []
        for md, line in commands:
            head, args = command_args(line)
            if SKILL in md.parents and head[-1] != "scripts/sprite_tool.py":
                bad.append(f"{md.relative_to(SCAN_ROOT)}: run it as scripts/sprite_tool.py from the skill: {line}")
                continue
            if not args:
                continue   # the general form, "python3 scripts/sprite_tool.py ..."
            quiet = io.StringIO()
            try:
                with contextlib.redirect_stdout(quiet), contextlib.redirect_stderr(quiet):
                    parser.parse_args(args)
            except SystemExit as stop:
                if stop.code:
                    bad.append(f"{md.relative_to(SCAN_ROOT)}: {line}: {quiet.getvalue().strip().splitlines()[-1]}")
        self.assertEqual(bad, [])


class Sprites(unittest.TestCase):
    """The templates, examples and bundled drawings lint clean and match their recorded pixels."""

    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory()
        cls.env = clean_env(cls.scratch.name)

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def check(self, *specs):
        result = run_tool(["check"] + list(specs), self.env)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_templates_and_examples_pass(self):
        for specs in (["templates/*.sprite"], ["examples/kirupa-portrait/*.sprite"],
                      ["examples/python-module/tangerine.py:TANGERINE16,TANGERINE24"]):
            result = self.check(*specs)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("ERROR", result.stdout)

    def test_module_tables(self):
        """Module drawings named by code are compared with the set, whether a table registers them with keys of
        another name or they are an exported ROWS_/KEYS_ pair."""
        example = {}
        exec(read(SKILL / "examples" / "python-module" / "tangerine.py"), example)
        module = Path(self.scratch.name) / "drawings.py"
        module.write_text(
            "from PIL import Image\n\n"
            f"ROWS_1F34A = {example['ROWS_TANGERINE16']!r}\n"
            f"TANGERINE_KEYS = {example['KEYS_TANGERINE16']!r}\n\n\n"
            "def art(rows, keys):\n"
            "    def build():\n"
            "        image = Image.new('RGBA', (len(rows), len(rows)))\n"
            "        for y, row in enumerate(rows):\n"
            "            for x, key in enumerate(row):\n"
            "                if key != '.':\n"
            "                    color = '#000000' if key == '#' else keys[key]\n"
            "                    image.putpixel((x, y), tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) + (255,))\n"
            "        return image\n"
            "    return build\n\n\n"
            "OBJECTS = {'1f34a': {16: art(ROWS_1F34A, TANGERINE_KEYS)}}\n", encoding="utf-8")
        result = self.check(f"{module}:1f34a")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("same as set:16:1f34a (", result.stdout)
        exported = Path(self.scratch.name) / "exported.py"
        exported.write_text(f"ROWS_1F34A = {example['ROWS_TANGERINE16']!r}\n"
                            f"KEYS_1F34A = {example['KEYS_TANGERINE16']!r}\n", encoding="utf-8")
        result = self.check(f"{exported}:1f34a")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("same as set:16:1f34a (", result.stdout)

    def test_module_small_by_meaning(self):
        """A module drawing named only by code takes its subject's name, so a 'small … square' may span under the
        floor without a set to compare with, while the same square under another name still fails."""
        rows = ["." * 16] * 4 + ["...." + "#" * 9 + "..."] + ["....#" + "s" * 7 + "#..."] * 7 \
            + ["...." + "#" * 9 + "..."] + ["." * 16] * 3
        module = Path(self.scratch.name) / "squares.py"
        module.write_text(f"ROWS_25FE = {rows!r}\nKEYS_25FE = {{'s': '#3a4148'}}\n"
                          f"ROWS_2B1B = {rows!r}\nKEYS_2B1B = {{'s': '#3a4148'}}\n", encoding="utf-8")
        result = self.check(f"{module}:25fe")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("small by meaning", result.stdout)
        result = self.check(f"{module}:2b1b")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("spans only 9x9px", result.stdout)

    def test_reference_library_passes(self):
        result = self.check("assets/reference/16/*.sprite", "assets/reference/24/*.sprite")
        self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr)
        self.assertEqual(result.stdout.count("(16px): ok") + result.stdout.count("(24px): ok"),
                         len(list((SKILL / "assets/reference").glob("*/*.sprite"))))

    def test_lint_failures_fail(self):
        failures = sorted((SKILL / "examples" / "lint-failures").glob("*.sprite"))
        self.assertGreater(len(failures), 0)
        for path in failures:
            result = self.check(str(path.relative_to(SKILL)))
            self.assertEqual(result.returncode, 1, path.name)
            self.assertIn("ERROR", result.stdout, path.name)

    def test_catalog_round_trips(self):
        st = tool()
        catalog = json.loads(read(SKILL / "assets" / "reference" / "catalog.json"))
        icons = catalog["icons"]
        self.assertEqual(catalog["count"], len(icons))
        expected = set()
        for size in (16, 24):
            listed = [i for i in icons if size in i["sizes"]]
            self.assertLessEqual(len(listed), 250, f"a study library, not the set ({size}px)")
            for item in listed:
                path = SKILL / "assets" / "reference" / str(size) / f"{item['code']}-{item['slug']}.sprite"
                expected.add(path)
                image = st.parse_sprite(path).image()
                self.assertEqual(image.size, (size, size), path.name)
                digest = hashlib.sha256(image.tobytes()).hexdigest()
                self.assertEqual(digest, item["pixelSha256"][str(size)], f"{path.name} differs from the set")
        on_disk = set((SKILL / "assets" / "reference").glob("*/*"))
        self.assertEqual(sorted(p.name for p in on_disk - expected), [], "files the catalog doesn't list")

    def test_cited_set_sprites_resolve(self):
        st = tool()
        saved = os.environ.pop("PIXEL_EMOJI_SET_DIR", None)
        st.OPTIONS.set_dirs = ()
        try:
            cited = set()
            for path in text_files(SKILL):
                for size, ident in re.findall(r"\bset:(16|24):([0-9a-z][0-9a-z-]*)", read(path)):
                    cited.add((int(size), ident))
            self.assertGreater(len(cited), 30)
            bad = []
            for size, ident in sorted(cited):
                try:
                    st.set_sprite(size, ident)
                except st.SpriteError as error:
                    bad.append(str(error)[:80])
            self.assertEqual(bad, [])
        finally:
            if saved is not None:
                os.environ["PIXEL_EMOJI_SET_DIR"] = saved


@unittest.skipUnless(IN_REPO, "repository files aren't part of an installed skill")
class Repository(unittest.TestCase):
    """The README's quick start runs offline on a fresh machine, and CI covers every platform."""

    def quickstart(self):
        text = read(ROOT / "README.md")
        match = re.search(r"<!-- quickstart:start -->(.*?)<!-- quickstart:end -->", text, re.S)
        self.assertIsNotNone(match, "README.md marks its quick start")
        lines = []
        for block in code_blocks(match.group(1)):
            for line in block.splitlines():
                line = line.strip()
                if "sprite_tool.py" in line and not line.startswith("#"):
                    lines.append(line)
        return lines

    def test_quickstart_runs_offline(self):
        lines = self.quickstart()
        self.assertGreaterEqual(len(lines), 5)
        before = sorted(p.relative_to(SKILL) for p in SKILL.rglob("*"))
        with tempfile.TemporaryDirectory() as scratch:
            env = clean_env(scratch)
            for line in lines:
                head, args = command_args(line)
                if head[-1].replace("\\", "/") != "scripts/sprite_tool.py":
                    self.fail(f"run quick-start commands from the skill folder: {line}")
                result = run_tool(args, env)
                output = result.stdout + result.stderr
                self.assertNotIn("Traceback", output, line)
                if args[0] in ("twemoji", "emoji") and result.returncode == 2:
                    self.assertTrue(result.stderr.startswith("error: "), output)
                    continue
                self.assertEqual(result.returncode, 0, f"{line}\n{output}")
            self.assertTrue(any(Path(env["PIXEL_EMOJI_WORK"]).iterdir()), "bare --out names go to the work folder")
        self.assertEqual(sorted(p.relative_to(SKILL) for p in SKILL.rglob("*")), before,
                         "the quick start must not write into the skill folder")

    def test_ci_matrix(self):
        workflow = read(ROOT / ".github" / "workflows" / "test.yml")
        for word in ("ubuntu-latest", "macos-latest", "windows-latest", "3.9", "3.13", "unittest discover"):
            self.assertIn(word, workflow)

    def test_licenses(self):
        self.assertIn("MIT License", read(ROOT / "LICENSE"))
        self.assertIn("MIT License", read(SKILL / "LICENSE.txt"))
        self.assertIn("CC BY 4.0", read(SKILL / "assets" / "LICENSE.md"))


def tearDownModule():
    junk = [p for p in SKILL.rglob("*") if p.name in ("__pycache__", ".DS_Store", "node_modules")]
    if junk:
        raise AssertionError(f"the tests left files in the skill folder: {junk}")


if __name__ == "__main__":
    unittest.main()
