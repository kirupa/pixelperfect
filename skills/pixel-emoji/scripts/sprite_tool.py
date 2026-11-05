#!/usr/bin/env python3
"""Draw, check and review hand-made 16x16 and 24x24 pixel emoji.

Run it from the skill folder (the one that holds SKILL.md) as python3 scripts/sprite_tool.py, or give the
script's full path from anywhere. On Windows, type py or python instead of python3. Below, T stands for it.

A bare --out file name (no folder in it) is written to the work folder, PIXEL_EMOJI_WORK (default
~/pixel-emoji-work); write ./NAME for the current folder. A bare input name is read from the current folder,
or else from the work folder. Quote arguments that hold commas, @ or #, e.g. "photo.jpg@300,375,445,410".

  T find WORD...                                  reference drawings to study: code, file name, name
  T new NAME --size 16 [--template smiley-head-16] --out NAME-16.sprite
  T mirror SPRITE --out NAME-16-r2.sprite [--axis 15] [--swap S=t] [--only "#."]   copy one half onto the other
  T check SPRITE...                               lint against the house rules; exit 1 on errors
  T check SPRITE --skin "S,s,t,u" --face "PHOTO@X0,Y0,X1,Y1"   also: is the skin within 15 luminance of the photo?
  T zoom SPRITE... --out zoom-r1.png
  T sheet SPRITE... --out sheet-r1.png [--ref IMAGE]... [--twemoji CODE]... [--emoji CODE]...
                                                  [--neighbor SPRITE]...
  T blind SPRITE... --control SPRITE... --out blind-r1 [--seed N]   shuffled letters for fresh reviewers
  T render SPRITE --out NAME.png [--scale N]
  T text SPRITE...                                any sprite as .sprite text, to study it
  T export SPRITE --name NAME                     the sprite as ROWS_NAME and KEYS_NAME Python lists
  T draft IMAGE --size 16 [--crop X0,Y0,X1,Y1] [--clear HEX]   (IMAGE@X0,Y0,X1,Y1 also crops)
  T crop "IMAGE@X0,Y0,X1,Y1" --scale 3 --out crop.png   check a box before you sample or draw
  T sample IMAGE --box X0,Y0,X1,Y1                the dominant colours in a box
  T sample PHOTO --box X0,Y0,X1,Y1 --face         on a clean patch of cheek or forehead: skin, flash, shadow, base
  T ramp HEX
  T twemoji CODE --out twemoji.png [--size 160]   the Twemoji original
  T emoji CODE --out emoji.png [--size 160]       this computer's colour emoji

IMAGE and PHOTO can be a file or an http(s) URL, which is downloaded once into the cache.
"""

SOURCES = """\
SPRITE can be:
  NAME.sprite         a .sprite text file (header 'key: value' lines, [palette], [grid])
  NAME.png            a 16x16 or 24x24 PNG with binary alpha
  set:SIZE:CODE       an approved drawing from the kirupa.com Pixel set, by Twemoji code or file name, e.g.
                      set:16:1f642 or set:24:skull-and-crossbones. It is read from --set-dir folders first
                      (or PIXEL_EMOJI_SET_DIR), then from the skill's reference library (assets/reference/,
                      about 250 subjects at both sizes; find lists them)
  MODULE.py:NAME,...  drawings kept in a Python module, as ROWS_NAME and KEYS_NAME lists (what export
                      prints), e.g. examples/python-module/tangerine.py:TANGERINE16. NAME can also be a key of a
                      dict OBJECTS, SPRITES, FACES or SPECIAL whose values are functions that take no arguments
                      and return a PIL image (or a {size: function} dict), or of BUILDERS, whose functions take
                      the size. Loading a module runs its code, so load only modules you trust.

Settings (all optional; the command-line options win):
  PIXEL_EMOJI_WORK         where bare --out names go (default ~/pixel-emoji-work)
  PIXEL_EMOJI_SET_DIR      folders or zips of a Pixel set's PNGs, named by code or file name, for set: and
                           find; separate several with the system path separator (: or ;). Like --set-dir
  PIXEL_EMOJI_TWEMOJI_DIR  folders or zips of Twemoji <code>.svg files, read before the cache and the CDN
  PIXEL_EMOJI_CACHE        where downloads are kept (default: the system cache folder, in pixel-emoji/)
  PIXEL_EMOJI_OFFLINE=1    never download; like --offline
  PIXEL_EMOJI_FONT         a colour emoji font file for the emoji command

Needs Python 3.9+, Pillow and numpy. Optional: resvg_py renders Twemoji SVGs (twemoji, sheet --twemoji), and
fontTools finds Apple Color Emoji's pictures of joined sequences (emoji 1f468-200d-1f373).
"""

import argparse
import colorsys
import functools
import glob
import hashlib
import importlib.util
import json
import os
import random
from collections import Counter
from io import BytesIO
from pathlib import Path
import re
import struct
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, features

sys.dont_write_bytecode = True   # loading a drawing module must not leave __pycache__ folders behind
SKILL = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL / "templates"
REFERENCE = SKILL / "assets" / "reference"
FULL_SET = "https://www.kirupa.com/tools/icon_gallery_pixel.htm"
INK_LUM = 40      # darker than this counts as ink, so #111111 can't fake the inner-ink rule
DARK_EDGE = 70    # at 16px a pixel darker than this may be its own edge: a thin stem, a strand of hair
LIGHT = (255, 255, 255)
DARK = (24, 26, 32)
TWEMOJI_VERSION = "17.0.3"
CDN = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@v" + TWEMOJI_VERSION + "/assets/svg/{}.svg"
USER_AGENT = "pixel-emoji-skill (+https://github.com/kirupa/pixelart)"
KEYS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
# Calibrated on the 1,948 approved drawings of the kirupa.com Pixel set at each size: none raises an error, each
# warning fires on at most ~6% of them, and 74% (16px) and 83% (24px) raise no warning at all. About 95% stay
# under inner_warn. hug_error: approved 16px art never has more than 13 hugging pixels, while a doubled outline
# has 20+; at 24px dark materials (cameras, a black cat) legitimately reach 54.
LIMITS = {
    16: {"span_error": 13, "span_warn": 14, "inner_warn": 0.12, "inner_error": 0.22, "hug": 7, "hug_error": 16,
         "colors": 14, "block": 2, "mirror": 4, "specks": 2, "pairs": 4},
    24: {"span_error": 17, "span_warn": 20, "inner_warn": 0.22, "inner_error": None, "hug": 24, "hug_error": None,
         "colors": 18, "block": 3, "mirror": 6, "specks": 2, "pairs": 6},
}
SMALL = re.compile(r"\bsmall\b.*\b(square|diamond)\b", re.I)   # 'small blue diamond': there, small is the meaning
WINDOWS_FONTS = Path(os.environ.get("WINDIR") or "C:/Windows") / "Fonts"
EMOJI_FONTS = ("/System/Library/Fonts/Apple Color Emoji.ttc",
               "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
               "/usr/share/fonts/noto/NotoColorEmoji.ttf",
               "/usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf",
               "/usr/share/fonts/google-noto-color-emoji-fonts/NotoColorEmoji.ttf",
               "/usr/share/fonts/noto-color-emoji/NotoColorEmoji.ttf",
               str(WINDOWS_FONTS / "seguiemj.ttf"))
EMOJI_PX = (160, 109, 128, 96, 64)   # colour bitmap fonts load only at their own sizes: Apple 160, Noto 109
LABEL_FONTS = ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf",
               "/usr/share/fonts/TTF/DejaVuSans.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
               str(WINDOWS_FONTS / "arial.ttf"), str(WINDOWS_FONTS / "segoeui.ttf"), "DejaVuSans.ttf", "Arial.ttf")


class SpriteError(Exception):
    pass


# ---------------------------------------------------------------- colour helpers

def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def color_arg(text, option):
    if not re.fullmatch(r"#?[0-9a-fA-F]{6}", text or ""):
        raise SpriteError(f"{option} {text!r}: give a colour as #rrggbb, e.g. #f4900c")
    return "#" + text.lstrip("#").lower()


def rgb_hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in rgb)


def lum(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def luminance(a):
    a = a.astype(float)
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def hsv(rgb):
    return colorsys.rgb_to_hsv(*(v / 255 for v in rgb))


def box(text):
    try:
        x0, y0, x1, y1 = (int(v) for v in text.split(","))
    except ValueError:
        raise SpriteError(f"--box/--crop takes X0,Y0,X1,Y1 in image pixels, not {text!r}")
    return x0, y0, x1, y1


# ---------------------------------------------------------------- files, settings and downloads

class Options:
    set_dirs = ()      # --set-dir values, searched before PIXEL_EMOJI_SET_DIR
    offline = False    # --offline


OPTIONS = Options()


def env_flag(name):
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def offline():
    return OPTIONS.offline or env_flag("PIXEL_EMOJI_OFFLINE")


def env_paths(name):
    return [Path(part.strip()).expanduser() for part in os.environ.get(name, "").split(os.pathsep) if part.strip()]


def cache_dir():
    """PIXEL_EMOJI_CACHE, or pixel-emoji/ in the system's cache folder."""
    if os.environ.get("PIXEL_EMOJI_CACHE"):
        return Path(os.environ["PIXEL_EMOJI_CACHE"]).expanduser()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "pixel-emoji"
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA")
        return (Path(base) if base else Path.home() / "AppData" / "Local") / "pixel-emoji"
    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache").expanduser() / "pixel-emoji"


def work_dir():
    return Path(os.environ.get("PIXEL_EMOJI_WORK") or "~/pixel-emoji-work").expanduser()


def bare(text):
    """A file name with no folder in it."""
    return not re.search(r"[/\\:]", text) and not text.startswith("~")


def out_path(text):
    """Where an --out goes: a bare name into the work folder, anything else as given. Makes missing folders."""
    path = work_dir() / text if bare(text) else Path(text).expanduser()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise SpriteError(f"can't make the folder {path.parent} ({error}); give --out a folder you can write to,"
                          " or set PIXEL_EMOJI_WORK")
    return path


def in_path(text):
    """An input file as given; a bare name that isn't in the current folder is read from the work folder."""
    path = Path(text).expanduser()
    if bare(text):
        there = work_dir() / text
        if not path.exists() and there.exists():
            return there
        if path.exists() and there.exists() and path.resolve() != there.resolve():
            print(f"note: reading ./{text}; the work folder has a {text} too ({there})", file=sys.stderr)
    return path


def fetch(url, timeout=30):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def why(error):
    reason = str(getattr(error, "reason", error))
    if "CERTIFICATE_VERIFY_FAILED" in reason:
        reason += "; with python.org's Python on macOS, run its Install Certificates command once"
    return reason


def save_cache(path, data):
    """Keep a download; True if it was saved. A cache that can't be written costs only the next download."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        part = path.with_name(path.name + ".part")
        part.write_bytes(data)
        os.replace(str(part), str(path))
        return True
    except OSError as error:
        print(f"note: can't write the cache {path.parent} ({error}); set PIXEL_EMOJI_CACHE to a folder you can"
              " write to", file=sys.stderr)
        return False


def url_image(url):
    """An http(s) image: the cached copy, or a fresh download that is cached for next time."""
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"):
        suffix = ".img"
    path = cache_dir() / "images" / (hashlib.sha1(url.encode("utf-8")).hexdigest()[:20] + suffix)
    if path.is_file():
        return path
    if offline():
        raise SpriteError(f"{url} isn't in the cache ({path.parent}) and downloads are off (--offline or"
                          " PIXEL_EMOJI_OFFLINE). Run the command once online, or save the image and give its"
                          " file path")
    try:
        data = fetch(url)
    except urllib.error.HTTPError as error:
        raise SpriteError(f"{url}: the server answered {error.code}; check the address, or save the image and give"
                          " its file path")
    except (urllib.error.URLError, OSError) as error:
        raise SpriteError(f"can't download {url} ({why(error)}); save the image and give its file path")
    return path if save_cache(path, data) else BytesIO(data)


def open_image(spec, area=None):
    """An image file or http(s) URL as RGBA, cropped to AREA or to an 'IMAGE@X0,Y0,X1,Y1' suffix (image pixels)."""
    path, suffix = spec, None
    url = re.match(r"(?i)https?://", spec)
    m = re.fullmatch(r"(.+)@(\d+,\d+,\d+,\d+)", spec)
    if m and (url or not in_path(spec).exists()):
        path, suffix = m.groups()
    if suffix and area:
        raise SpriteError(f"{spec}: give the crop once, as @X0,Y0,X1,Y1 or as --crop/--box")
    area = suffix or area
    if url:
        source = url_image(path)
    else:
        source = in_path(path)
        if not source.is_file():
            raise SpriteError(f"{path}: no such image")
    try:
        with Image.open(source) as image:
            image = (ImageOps.exif_transpose(image) or image).convert("RGBA")   # phone photos store their turn in EXIF
    except OSError:
        raise SpriteError(f"{path}: not an image Pillow can read")
    image.info["full_size"] = image.size
    if area:
        x0, y0, x1, y1 = box(area)
        if not (0 <= x0 < x1 <= image.width and 0 <= y0 < y1 <= image.height):
            raise SpriteError(f"{area} is not inside the {image.width}x{image.height} image {path}"
                              " (X0,Y0,X1,Y1 with X0 < X1 and Y0 < Y1)")
        full = image.size
        image = image.crop((x0, y0, x1, y1))
        image.info["full_size"] = full
    return image


def image_name(spec):
    """A short label for an image file or URL, keeping any @box."""
    return re.split(r"[/\\]", spec.rstrip("/\\"))[-1] or spec


# ---------------------------------------------------------------- sprites

class Sprite:
    """A square drawing: rows of one-character keys and a palette. '#' is ink #000000, '.' is clear."""

    def __init__(self, name, rows, palette, meta=None, origin="", problems=None):
        self.name, self.rows, self.palette = name, rows, palette
        self.meta = meta or {}
        self.origin = origin or name
        self.problems = problems or []   # defects found while loading; lint reports them as errors
        self.status = ""                 # MODULE.py: sources say whether they match the published icon

    @property
    def size(self):
        return len(self.rows)

    def image(self):
        n = self.size
        a = np.zeros((n, n, 4), np.uint8)
        for y, row in enumerate(self.rows):
            for x, key in enumerate(row):
                if key == "#":
                    a[y, x] = (0, 0, 0, 255)
                elif key != ".":
                    a[y, x] = hex_rgb(self.palette[key][0]) + (255,)
        return Image.fromarray(a)

    def label(self):
        rev = self.meta.get("rev")
        return f"{self.name} {self.size}px" + (f" rev {rev}" if rev else "")

    def text(self):
        lines = [f"// {self.status}"] if self.status else []
        lines += [f"name: {self.name}", f"size: {self.size}"]
        lines += [f"{k}: {v}" for k, v in self.meta.items() if k not in ("name", "size")]
        lines += ["", "[palette]"]
        if not self.palette:
            lines.append("// one line per colour, KEY #rrggbb what it is, e.g.: o #f4900c orange base."
                         " '#' (ink, #000000) and '.' (clear) are built in")
        width = max([len(rgb_hex(hex_rgb(h))) for h, _ in self.palette.values()] or [7])
        for key, (color, what) in sorted(self.palette.items(), key=lambda kv: lum(hex_rgb(kv[1][0]))):
            lines.append(f"{key} {color:<{width}} {what}".rstrip())
        lines += ["", "[grid]"] + self.rows
        return "\n".join(lines) + "\n"


def parse_sprite(path):
    """Read a .sprite file: 'key: value' lines, then [palette] and [grid]. '//' at the start of a line or after a
    space starts a comment (so 'reference: https://...' survives)."""
    path = Path(path)
    meta, palette, rows, section = {}, {}, [], None
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = re.split(r"(?:^|\s)//", raw, 1)[0].strip()
        where = f"{path}:{number}"
        if not line:
            continue
        if line in ("[palette]", "[grid]"):
            section = line[1:-1]
        elif section is None:
            key, sep, value = line.partition(":")
            if not sep:
                raise SpriteError(f"{where}: before [palette] and [grid], lines are 'key: value'")
            meta[key.strip().lower()] = value.strip()
        elif section == "palette":
            parts = line.split(None, 2)
            if len(parts) < 2 or len(parts[0]) != 1 or not re.fullmatch(r"#[0-9a-fA-F]{6}", parts[1]):
                raise SpriteError(f"{where}: palette lines are '<one-character key> <#rrggbb> <what it is>'")
            if parts[0] in "#.":
                raise SpriteError(f"{where}: '#' is always ink (#000000) and '.' always clear; pick another key")
            if parts[0] in palette:
                raise SpriteError(f"{where}: key {parts[0]!r} is defined twice")
            palette[parts[0]] = (parts[1].lower(), parts[2] if len(parts) > 2 else "")
        else:
            rows.append((number, line))
    if not rows:
        raise SpriteError(f"{path}: no [grid] rows")
    n = len(rows)
    if n not in (16, 24):
        raise SpriteError(f"{path}: {n} grid rows; sprites are 16x16 or 24x24")
    if "size" in meta and meta["size"] != str(n):
        raise SpriteError(f"{path}: size: {meta['size']} but the grid has {n} rows")
    for number, row in rows:
        if len(row) != n:
            raise SpriteError(f"{path}:{number}: row is {len(row)} wide, not {n}: {row}")
        unknown = sorted(set(row) - set(palette) - set("#."))
        if unknown:
            raise SpriteError(f"{path}:{number}: keys {' '.join(unknown)} are not in [palette]")
    name = meta.pop("name", path.stem)
    meta.pop("size", None)
    return Sprite(name, [row for _, row in rows], palette, meta, origin=str(path))


def from_image(image, name, origin=""):
    a = np.asarray(image.convert("RGBA"))
    n = a.shape[0]
    if a.shape[0] != a.shape[1] or n not in (16, 24):
        raise SpriteError(f"{name}: {a.shape[1]}x{a.shape[0]}; sprites are 16x16 or 24x24")
    if not np.isin(a[..., 3], (0, 255)).all():
        raise SpriteError(f"{name}: partial transparency. Pixel art is binary: every pixel fully clear or fully"
                          " opaque, with no anti-aliasing")
    problems = []
    if a[a[..., 3] == 0].any():
        problems.append("transparent pixels carry colour; save them as (0,0,0,0)")
    colors = sorted({tuple(int(v) for v in p[:3]) for p in a.reshape(-1, 4) if p[3] == 255} - {(0, 0, 0)}, key=lum)
    if len(colors) > len(KEYS):
        raise SpriteError(f"{name}: {len(colors)} colours; that is a photo, not a sprite")
    keyof = {c: KEYS[i] for i, c in enumerate(colors)}
    rows = []
    for y in range(n):
        row = ""
        for x in range(n):
            r, g, b, alpha = (int(v) for v in a[y, x])
            row += "." if alpha == 0 else "#" if (r, g, b) == (0, 0, 0) else keyof[(r, g, b)]
        rows.append(row)
    return Sprite(name, rows, {k: (rgb_hex(c), "") for c, k in keyof.items()}, {}, origin, problems)


# ---------------------------------------------------------------- the Pixel set and the reference library

@functools.lru_cache(maxsize=None)
def reference_catalog():
    """{code: item} for the skill's bundled reference library (assets/reference/catalog.json)."""
    path = REFERENCE / "catalog.json"
    if not path.is_file():
        return {}
    return {item["code"]: item for item in json.loads(path.read_text(encoding="utf-8"))["icons"]}


def reference_item(ident):
    found = reference_catalog()
    return found.get(ident) or next((item for item in found.values() if item["slug"] == ident), None)


def code_name(ident):
    """A subject's name for a code: the reference library's, else Unicode's own name for one emoji code point
    (so 'FACE' or 'cafe' as a drawing's name never become CJK or Hangul characters)."""
    item = reference_item(ident)
    if item:
        return item["name"]
    point = int(ident, 16) if re.fullmatch(r"[0-9a-f]{2,6}", ident) else -1
    if point in (0xA9, 0xAE) or 0x2000 <= point <= 0x33FF or 0x1F000 <= point <= 0x1FAFF:
        return unicodedata.name(chr(point), "").lower()
    return ""


def catalog_entry(item, where, size=None):
    """One subject, from either catalog format: {code, slug, name, keywords, category, sizes, where}."""
    code = item.get("code") or item.get("path") or ""
    sizes = item.get("sizes") or ([size] if size else [])
    return {"code": code, "slug": item.get("slug") or item.get("file") or "",
            "name": item.get("name") or item.get("label") or "", "keywords": item.get("keywords", ""),
            "category": item.get("category", ""), "sizes": sizes, "where": where}


class SetSource:
    """A folder or zip of a Pixel set's PNGs, named by Twemoji code or file name, with an optional catalog.json:
    the free PNG download from the Icon Gallery (zipped or not), its png/ folder, or your own set."""

    def __init__(self, text):
        self.text = str(text)
        self.path = Path(text).expanduser()
        self.zip = None
        if self.path.is_file() and zipfile.is_zipfile(str(self.path)):
            self.zip = zipfile.ZipFile(str(self.path))
        elif not self.path.is_dir():
            raise SpriteError(f"{self.text} (from --set-dir or PIXEL_EMOJI_SET_DIR) is not a folder or a zip")
        self.files = {}      # lower-case name without .png: [file or zip member]
        for name, ref in self._pngs():
            self.files.setdefault(name.lower(), []).append(ref)
        self.items = self._catalog()

    def _pngs(self):
        if self.zip:
            for member in self.zip.namelist():
                if member.lower().endswith(".png") and "__MACOSX" not in member:
                    yield member.rsplit("/", 1)[-1][:-4], member
            return
        for sub in ("", "png", "16", "24"):
            folder = self.path / sub
            if folder.is_dir():
                for entry in os.scandir(str(folder)):
                    if entry.name.lower().endswith(".png") and entry.is_file():
                        yield entry.name[:-4], Path(entry.path)

    def _catalog(self):
        """[(entry, size)] from catalog.json beside the PNGs (or one folder up from png/)."""
        text = None
        if self.zip:
            names = [m for m in self.zip.namelist() if m.rsplit("/", 1)[-1] == "catalog.json"]
            if names:
                text = self.zip.read(min(names, key=len)).decode("utf-8")
        else:
            for path in (self.path / "catalog.json", self.path.parent / "catalog.json"):
                if path.is_file() and (path.parent == self.path or self.path.name.lower() == "png"):
                    text = path.read_text(encoding="utf-8")
                    break
        if not text:
            return []
        try:
            data = json.loads(text)
            size = data.get("size")
            return [(catalog_entry(item, self.text, size), size) for item in data["icons"]]
        except (ValueError, KeyError, TypeError, AttributeError):
            print(f"note: {self.text} has a catalog.json this tool can't read; it uses the file names only",
                  file=sys.stderr)
            return []

    def names(self, ident):
        """File names that may hold IDENT: itself, and its code or file name from this set's catalog and the
        reference library."""
        found = [ident]
        for entry, _ in self.items:
            if ident in (entry["code"], entry["slug"]):
                found += [entry["code"], entry["slug"]]
        item = reference_item(ident)
        if item:
            found += [item["code"], item["slug"]]
        if "-fe0f" in ident:
            found.append(ident.replace("-fe0f", ""))
        return [n for i, n in enumerate(found) if n and n not in found[:i]]

    def image(self, size, ident):
        """(RGBA image, the name to show, other sizes seen) for IDENT at SIZE, or (None, None, sizes)."""
        seen = set()
        for name in self.names(ident):
            for ref in self.files.get(name.lower(), []):
                try:
                    data = self.zip.read(ref) if self.zip else ref.read_bytes()
                    with Image.open(BytesIO(data)) as png:
                        if png.size != (size, size):
                            if png.size[0] == png.size[1] and png.size[0] in (16, 24):
                                seen.add(png.size[0])
                            continue
                        image = png.convert("RGBA")
                except OSError:
                    continue
                entry = next((e for e, s in self.items if name in (e["code"], e["slug"]) and s in (None, size)),
                             None)
                item = reference_item(name)
                code = (entry or {}).get("code") or (item or {}).get("code") or name
                label = (entry or {}).get("name") or (item or {}).get("name") or name.replace("-", " ")
                return image, f"{label} ({code})", seen
        return None, None, seen

    def entries(self, size):
        if self.items:
            return [entry for entry, s in self.items if s in (None, size)]
        out = []
        for name in sorted(self.files):
            code = name if re.fullmatch(r"[0-9a-f]{4,6}(-[0-9a-f]{4,6})*", name) else ""
            item = reference_item(name) or {}
            out.append({"code": code or item.get("code", ""), "slug": item.get("slug", "" if code else name),
                        "name": item.get("name") or name.replace("-", " "), "keywords": "",
                        "category": item.get("category", ""), "sizes": [], "where": self.text})
        return out


@functools.lru_cache(maxsize=None)
def set_source(text):
    return SetSource(text)


def set_sources():
    texts = list(OPTIONS.set_dirs) + [str(p) for p in env_paths("PIXEL_EMOJI_SET_DIR")]
    return [set_source(t) for i, t in enumerate(texts) if t not in texts[:i]]


def set_sprite(size, ident, spec=None):
    """An approved drawing as a Sprite: from the --set-dir folders and zips first, then the reference library."""
    if size not in (16, 24):
        raise SpriteError(f"set:{size}:{ident}: the sets are 16 and 24px")
    ident = emoji_code(ident)
    spec = spec or f"set:{size}:{ident}"
    seen = set()
    for source in set_sources():
        image, label, sizes = source.image(size, ident)
        if image is not None:
            sprite = from_image(image, label, spec)
            sprite.meta["source"] = source.text
            return sprite
        seen |= sizes
    item = reference_item(ident)
    if item and size in item["sizes"]:
        sprite = parse_sprite(REFERENCE / str(size) / f"{item['code']}-{item['slug']}.sprite")
        sprite.name, sprite.origin = f"{item['name']} ({item['code']})", spec
        return sprite
    if seen:
        where = f"; the set folders have it only at {', '.join(f'{s}px' for s in sorted(seen))}"
    elif item:
        where = f"; the reference library has it only at {', '.join(f'{s}px' for s in item['sizes'])}"
    else:
        where = ""
    raise SpriteError(
        f"set:{size}:{ident}: no such drawing{where}. The skill bundles {len(reference_catalog())} reference subjects"
        f" (find WORD lists them). For the whole set, download the free PNGs from {FULL_SET} and pass the zip or its"
        " folder with --set-dir, or name it in PIXEL_EMOJI_SET_DIR; any folder of 16 or 24px PNGs named by Twemoji"
        " code (1f642) or file name (slightly-smiling-face) works, including your own")


def module_builds(module, name, size):
    """{size or None: zero-argument build} for one subject, from a module's tables of build functions."""
    for table in ("OBJECTS", "SPRITES", "FACES", "SPECIAL"):
        builds = getattr(module, table, None)
        if isinstance(builds, dict) and name in builds:
            value = builds[name]
            return value if isinstance(value, dict) else {None: value}
    builders = getattr(module, "BUILDERS", None)     # build(size); 24px unless --size says otherwise
    if isinstance(builders, dict) and name in builders:
        return {s: functools.partial(builders[name], s) for s in ([size] if size else [24])}
    return None


def rows_sprite(module, path, name, rows, keys, size):
    """A sprite from ROWS_NAME (strings of one-character keys) and KEYS_NAME ({key: '#rrggbb'})."""
    where = f"{path}:{name}"
    if not isinstance(rows, (list, tuple)) or not rows or not all(isinstance(r, str) for r in rows):
        raise SpriteError(f"{where}: ROWS_{name} must be a list of strings")
    if not isinstance(keys, dict):
        raise SpriteError(f"{where}: KEYS_{name} must be a dict of key: '#rrggbb' (export prints one)")
    palette, remap = {}, {}
    free = iter(k for k in KEYS if k not in keys)
    for key, color in keys.items():
        if not (isinstance(key, str) and len(key) == 1 and isinstance(color, str)
                and re.fullmatch(r"#?[0-9a-fA-F]{6}", color)):
            raise SpriteError(f"{where}: KEYS_{name} entry {key!r}: {color!r} is not a one-character key and #rrggbb")
        color = "#" + color.lstrip("#").lower()
        if key == "#" and color == "#000000":
            continue
        if key in "#.":
            remap[key] = next(free)    # '#' and '.' are always ink and clear in a .sprite
            key = remap[key]
        palette[key] = (color, "")
    grid = ["".join(remap.get(k, k) for k in row) for row in rows]
    n = len(grid)
    if n not in (16, 24) or any(len(row) != n for row in grid):
        raise SpriteError(f"{where}: ROWS_{name} is not 16 rows of 16 or 24 rows of 24")
    unknown = sorted(set("".join(grid)) - set(palette) - set("#."))
    if unknown:
        raise SpriteError(f"{where}: keys {' '.join(unknown)} are in ROWS_{name} but not in KEYS_{name}")
    if size and size != n:
        raise SpriteError(f"{where} is {n}px, not {size}px")
    return Sprite(name.lower(), grid, palette, {}, where)


def module_sprites(path, names, size):
    path = in_path(path)
    if not path.is_file():
        raise SpriteError(f"{path}: no such module")
    folder = str(path.resolve().parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)      # so the module can import its neighbours
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as error:
        raise SpriteError(f"{path} fails to load: {type(error).__name__}: {error}")
    out = []
    for name in names:
        const = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")
        rows, keys = getattr(module, "ROWS_" + const, None), getattr(module, "KEYS_" + const, None)
        # export's ROWS_NAME and KEYS_NAME pair comes first. ROWS_NAME alone may be one half of a drawing that a
        # table registers with keys of another name, so the tables come next.
        builds = module_builds(module, name, size) if keys is None else None
        if rows is not None and builds is None:
            sprite = rows_sprite(module, path, const, rows, keys, size)
            if code_name(name):
                sprite.name = f"{code_name(name)} ({name})"
            set_status(sprite, sprite.image(), name)
            out.append(sprite)
            continue
        if builds is None:
            listed = sorted(k[5:] for k in vars(module) if k.startswith("ROWS_"))
            raise SpriteError(f"{path} has no ROWS_{const}, and no {name!r} in OBJECTS, SPRITES, FACES, SPECIAL or"
                              f" BUILDERS" + (f"; its ROWS_ names: {', '.join(listed[:12])}" if listed else ""))
        if size and None not in builds and size not in builds:
            raise SpriteError(f"{path} draws {name} at {sorted(builds)}px, not {size}px")
        for s in ([size] if size and size in builds else sorted(builds, key=lambda k: k or 0)):
            drawn = builds[s]()
            image = drawn.image if hasattr(drawn, "image") else drawn
            if not isinstance(image, Image.Image):
                raise SpriteError(f"{path}: {name}'s function returned {type(image).__name__}, not a PIL image")
            if size and image.width != size:
                raise SpriteError(f"{path} draws {name} at {image.width}px, not {size}px")
            sprite = from_image(image, f"{code_name(name) or name} ({name})", f"{path}:{name}")
            set_status(sprite, image, name)
            out.append(sprite)
    return out


def set_status(sprite, image, name):
    """Note whether a module's drawing matches the approved drawing of the same code, when there is one, and take
    that drawing's name, which the lint reads (a 'small … square' may be small)."""
    try:
        known = set_sprite(image.width, name)
    except SpriteError:
        return
    sprite.name = known.name
    same = np.array_equal(cleared(known.image()), cleared(image))
    where = known.meta.get("source", "the reference library")
    sprite.status = (f"same as set:{image.width}:{name} ({where})" if same else
                     f"differs from set:{image.width}:{name} ({where}): an unbuilt edit, or a"
                     f" drawing that set doesn't use at {image.width}px")


def cleared(image):
    a = np.array(image.convert("RGBA"))
    a[a[..., 3] == 0] = 0
    return a


def load(spec, size=None):
    """Every sprite named by SPEC (see SOURCES)."""
    if spec.startswith("set:"):
        parts = spec.split(":", 2)
        if len(parts) != 3 or not parts[1].isdigit() or not parts[2]:
            raise SpriteError(f"{spec!r}: write set:16:1f642 or set:24:slightly-smiling-face")
        return [set_sprite(int(parts[1]), parts[2], spec)]
    if ".py:" in spec:
        path, names = spec.split(".py:", 1)
        return module_sprites(path + ".py", [c for c in names.split(",") if c], size)
    path = in_path(spec)
    if not path.exists():
        raise SpriteError(f"{spec}: no such file" + (f" here or in the work folder {work_dir()}" if bare(spec) else ""))
    if path.suffix.lower() == ".sprite":
        return [parse_sprite(path)]
    try:
        with Image.open(path) as image:
            return [from_image(image, path.stem, str(path))]
    except OSError:
        raise SpriteError(f"{spec}: not a .sprite file or an image Pillow can read")


def expand(specs):
    """Expand *, ? and [..] in file sources (bash does this itself; PowerShell and cmd pass them through)."""
    out = []
    for spec in specs:
        if spec.startswith("set:") or ".py:" in spec or "://" in spec or not set("*?[") & set(spec) or Path(spec).exists():
            out.append(spec)
            continue
        hits = sorted(glob.glob(spec))
        if not hits and not Path(spec).is_absolute():
            hits = sorted(glob.glob(str(work_dir() / spec)))
        if not hits:
            raise SpriteError(f"{spec}: no files match")
        out.extend(hits)
    return out


def load_all(specs, size=None):
    return [s for spec in expand(specs) for s in load(spec, size)]


# ---------------------------------------------------------------- the house rules

def spots(mask, n=6):
    ys, xs = np.nonzero(mask)
    found = ", ".join(f"({x},{y})" for y, x in list(zip(ys, xs))[:n])
    return found + (" ..." if len(ys) > n else "")


def near(mask):
    p = np.pad(mask, 1)
    return p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]


def mirror_breaks(opaque, axis):
    """Silhouette pixels with no partner across x + x' = axis, as '(x,y)/(x',y)' (or '(x,y)/off-grid')."""
    n = opaque.shape[0]
    found = []
    for y in range(n):
        for x in range(n):
            xr = axis - x
            if 0 <= xr < n:
                if x < xr and opaque[y, x] != opaque[y, xr]:
                    found.append(f"({x},{y})/({xr},{y})")
            elif opaque[y, x]:
                found.append(f"({x},{y})/off-grid")
    return found


def mirror_score(opaque):
    """Fewest silhouette pixels that break a left-right mirror, over the axes x + x' = n-2, n-1 and n."""
    n = opaque.shape[0]
    best = None
    for axis in (n - 2, n - 1, n):
        bad = len(mirror_breaks(opaque, axis))
        if best is None or bad < best[0]:
            best = (bad, axis)
    return best


def lint(sprite):
    """(errors, warnings, stats). Errors break the style; warnings need a look but can be right on purpose."""
    n = sprite.size
    limits = LIMITS[n]
    a = np.asarray(sprite.image()).astype(int)
    opaque = a[..., 3] == 255
    if not opaque.any():
        return ["empty drawing"], [], {"notes": []}
    errors, warnings = [], []
    rgb, light = a[..., :3], luminance(a[..., :3])
    ink = opaque & (light < INK_LUM)
    exact = opaque & (rgb == 0).all(-1)
    clear = np.pad(~opaque, 1, constant_values=True)
    left, right, up, down = clear[1:-1, :-2], clear[1:-1, 2:], clear[:-2, 1:-1], clear[2:, 1:-1]
    beside = left | right | up | down
    thin = (left & right) | (up & down)
    inner = ink & ~beside
    bare = opaque & ~exact & beside
    errors += sprite.problems
    if n == 24:
        if bare.any():
            errors.append(f"{bare.sum()} coloured pixels touch transparency or the canvas edge (x,y): {spots(bare)}"
                          " -- at 24px every silhouette pixel is '#' ink, including spikes, drips and tears")
    else:
        lit = bare & (light >= DARK_EDGE)
        lines, lit = lit & thin, lit & ~thin
        dark = bare & (light < DARK_EDGE)
        if lit.any():
            errors.append(f"{lit.sum()} light pixels touch transparency or the canvas edge (x,y): {spots(lit)}"
                          " -- the silhouette needs its 1px '#' outline")
        if lines.any():
            warnings.append(f"{lines.sum()} pixels of unoutlined 1px lines (x,y): {spots(lines)} -- right only for"
                            " flat effects (steam, rays, sparkles, motion) in a mid tone that reads on white and dark")
        if dark.any():
            warnings.append(f"{dark.sum()} dark pixels are their own edge (x,y): {spots(dark)} -- right for a thin"
                            " dark stem, leaf tip, strand of hair or whisker; otherwise outline it")
    ys, xs = np.nonzero(opaque)
    w, h = int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)
    small = sprite.meta.get("scale", "").lower() == "small" or bool(SMALL.search(sprite.name.replace("-", " ")))
    if max(w, h) < limits["span_warn"] and small:
        warnings.append(f"the subject spans {w}x{h}px, allowed because it is small by meaning ('small' in its name or"
                        " 'scale: small'); keep the set's graded sizes")
    elif max(w, h) < limits["span_error"]:
        errors.append(f"the subject spans only {w}x{h}px; fill the canvas ({limits['span_warn']}-{n}px on the long"
                      " side)")
    elif max(w, h) < limits["span_warn"]:
        warnings.append(f"the subject spans {w}x{h}px; approved icons span {limits['span_warn']}-{n}px. Go bigger")
    ratio = inner.sum() / opaque.sum()
    if limits["inner_error"] and ratio > limits["inner_error"]:
        errors.append(f"{ratio:.0%} of the drawing is black inside the silhouette: blotchy. Separate parts with tones"
                      " and keep inner ink for holes, crevices, face features, overlaps of similar values and"
                      " line-art symbols")
    elif ratio > limits["inner_warn"]:
        warnings.append(f"{ratio:.0%} inner black (about 95% of approved {n}px icons stay under"
                        f" {limits['inner_warn']:.0%}): name the reason for every inner ink pixel or repaint it with"
                        " the part's darkest tone")
    hug = inner & near(ink & beside)
    if limits["hug_error"] and hug.sum() >= limits["hug_error"]:
        errors.append(f"{hug.sum()} inner black pixels sit right inside the outline (x,y): {spots(hug)} -- a doubled"
                      " outline. The outline is one pixel thick; repaint the inner ring with the material's dark tone")
    elif hug.sum() >= limits["hug"]:
        warnings.append(f"{hug.sum()} inner black pixels sit right inside the outline (x,y): {spots(hug)} -- a doubled"
                        " outline or a black seam? Use the material's dark tone instead")
    block = inner.copy()
    for _ in range(limits["block"] - 1):
        block = block[:-1, :-1] & block[1:, :-1] & block[:-1, 1:] & block[1:, 1:]
    if block.any():
        k = limits["block"]
        warnings.append(f"{k}x{k} black block inside the shape at (x,y): {spots(block, 3)} -- right for a hole, an open"
                        " mouth, an eye socket or a dark lens; otherwise it's a blotch")
    friends = sum(np.roll(np.roll(np.pad(ink, 1), dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                  if dy or dx)[1:-1, 1:-1]
    specks = ink & (friends == 0)
    if specks.sum() > limits["specks"]:
        warnings.append(f"{specks.sum()} lone black specks (x,y): {spots(specks)} -- a pair of 1x1 eyes, a pupil or a"
                        " nostril is fine; more is noise")
    colors = len({tuple(p) for p in rgb[opaque]})
    if colors > limits["colors"]:
        warnings.append(f"{colors} colours; nearly all approved {n}px icons use {limits['colors']} or fewer (median"
                        f" {7 if n == 16 else 8}). Merge ramps")
    key = np.where(opaque, rgb[..., 0] * 65536 + rgb[..., 1] * 256 + rgb[..., 2], -1)
    p = np.pad(key, 1, constant_values=-2)
    lone = opaque & ~ink & (p[:-2, 1:-1] != key) & (p[2:, 1:-1] != key) & (p[1:-1, :-2] != key) & (p[1:-1, 2:] != key)
    if lone.sum() / opaque.sum() > 0.15:
        warnings.append(f"{lone.sum()} single-pixel tone specks: noisy or dithered. Merge them into clean areas")
    same = Counter()
    for dy, dx in ((0, 1), (1, 0)):
        a1, a2 = rgb[:n - dy, :n - dx], rgb[dy:, dx:]
        both = opaque[:n - dy, :n - dx] & opaque[dy:, dx:] & ~ink[:n - dy, :n - dx] & ~ink[dy:, dx:]
        for y, x in zip(*np.nonzero(both & (a1 != a2).any(-1))):
            c1, c2 = tuple(int(v) for v in a1[y, x]), tuple(int(v) for v in a2[y, x])
            h1, s1, _ = hsv(c1)
            h2, s2, _ = hsv(c2)
            hue = min(abs(h1 - h2), 1 - abs(h1 - h2)) * 360
            if abs(lum(c1) - lum(c2)) < 14 and s1 > 0.3 and s2 > 0.3 and hue > 35:
                same[tuple(sorted((rgb_hex(c1), rgb_hex(c2))))] += 1
    if sum(same.values()) >= limits["pairs"]:
        pairs = ", ".join(f"{p[0]}/{p[1]} x{c}" for p, c in same.most_common())
        warnings.append(f"different colours of nearly equal value touch ({pairs}): they blur together at 1x and in"
                        " greyscale. Make one clearly lighter or darker, or ink the border")
    bad, axis = mirror_score(opaque)
    notes = []
    if 0 < bad <= limits["mirror"]:
        pairs = ", ".join(mirror_breaks(opaque, axis))
        broken = f"{bad} pixel{'s' if bad != 1 else ''} break{'s' if bad == 1 else ''} it"
        if sprite.meta.get("asymmetric"):
            notes.append(f"asymmetric (accepted): {sprite.meta['asymmetric']} -- mirror x + x' = {axis}: {broken}"
                         f" ({pairs})")
        else:
            warnings.append(f"nearly mirror-symmetric (axis x + x' = {axis}) but {broken} ({pairs}); fix"
                            f" {'it' if bad == 1 else 'them'} if the subject is symmetric, or name the reason in an"
                            " 'asymmetric:' header line")
    warnings += palette_notes(sprite)
    stats = {"inner": f"{ratio:.0%}", "colours": colors, "span": f"{w}x{h}", "mirror": f"x+x'={axis} ({bad} off)",
             "notes": notes}
    return errors, warnings, stats


def palette_notes(sprite):
    notes = []
    if not sprite.origin.endswith(".sprite") or sprite.meta.get("source"):
        return notes  # the authoring notes are for drawings in progress, not for approved art copied in with a source line
    if not sprite.meta.get("essence"):
        notes.append("no 'essence:' line. Write essence, keep and drop before you draw (SKILL.md, step 2)")
    used = set("".join(sprite.rows))
    unused = sorted(set(sprite.palette) - used)
    if unused:
        notes.append(f"palette keys never used: {' '.join(unused)}")
    seen = {}
    for key, (color, _) in sprite.palette.items():
        if lum(hex_rgb(color)) < INK_LUM:
            notes.append(f"key {key} {color} is darker than luminance {INK_LUM}, so it reads (and tests) as ink. Use '#'"
                         " for ink, or lift a black material to the slate ramp #262b30 / #30363c / #3a4148 / #66717c")
        if color in seen:
            notes.append(f"keys {seen[color]} and {key} are the same colour {color}")
        seen[color] = key
    return notes


# ---------------------------------------------------------------- rendering

@functools.lru_cache(maxsize=None)
def font(size=11):
    for path in LABEL_FONTS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)    # Pillow 10.1+
    except (TypeError, OSError, ImportError):
        return ImageFont.load_default()


def write_text_out(text, out, force=False, what="file"):
    """Write TEXT to OUT (a bare name goes to the work folder) with LF line ends; refuse to replace a file unless FORCE."""
    path = out_path(out)
    if path.exists() and not force:
        raise SpriteError(f"{path} exists; pass --force to replace it, or write the next rev {what}")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(path)
    return path


def save_image(image, out, note=""):
    """Write IMAGE to --out OUT (a bare name goes to the work folder) and print where it went."""
    path = out_path(out)
    if path.suffix.lower() in (".jpg", ".jpeg"):
        image = image.convert("RGB")
    try:
        image.save(str(path))
    except ValueError:
        raise SpriteError(f"{out}: end the file name in .png")
    except OSError as error:
        raise SpriteError(f"can't write {path} ({error})")
    print(f"{path}{': ' + note if note else ''}")
    return path


def scaled(image, k):
    return image.resize((image.width * k, image.height * k), Image.NEAREST)


def fit(image, w, h):
    image = image.convert("RGBA")
    k = min(w / image.width, h / image.height)
    if k >= 1 and float(k).is_integer():
        return image.resize((int(image.width * k), int(image.height * k)), Image.NEAREST)
    return image.resize((max(1, round(image.width * k)), max(1, round(image.height * k))), Image.LANCZOS)


def grid_tile(sprite, cell, labels=True):
    """The sprite at `cell` px per pixel on a faint grid, with both mirror axes and x/y numbers."""
    n, image = sprite.size, sprite.image()
    m = 16 if labels else 0
    S = n * cell
    tile = Image.new("RGB", (S + m, S + m), (250, 250, 250))
    d = ImageDraw.Draw(tile)
    small = font(9)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                d.rectangle((m + i * cell, m + j * cell, m + (i + 1) * cell - 1, m + (j + 1) * cell - 1),
                            fill=(238, 238, 238))
    big = scaled(image, cell)
    tile.paste(big, (m, m), big)
    over = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    o = ImageDraw.Draw(over)
    for k in range(n + 1):
        strong = k % 4 == 0
        color = (90, 90, 90, 90) if strong else (120, 120, 120, 45)
        o.line((m + k * cell, m, m + k * cell, m + S), fill=color)
        o.line((m, m + k * cell, m + S, m + k * cell), fill=color)
    half = n // 2
    o.line((m + half * cell, m, m + half * cell, m + S), fill=(40, 90, 230, 170), width=2)
    o.line((m + half * cell + cell // 2, m, m + half * cell + cell // 2, m + S), fill=(40, 90, 230, 70), width=1)
    tile = Image.alpha_composite(tile.convert("RGBA"), over).convert("RGB")
    if labels:
        d = ImageDraw.Draw(tile)
        step = 1 if cell >= 14 else 2
        for k in range(0, n, step):
            d.text((m + k * cell + 2, 2), str(k), fill=(60, 60, 60), font=small)
            d.text((1, m + k * cell + 1), str(k), fill=(60, 60, 60), font=small)
    return tile


def size_panel(images, background, scales=(1, 2, 3), pad=6):
    width = sum(max(i.width for i in images) * s + pad for s in scales) + pad
    height = max(i.height for i in images) * max(scales) * len(images) + pad * (len(images) + 1)
    panel = Image.new("RGB", (width, height), background)
    y = pad
    for image in images:
        x = pad
        for s in scales:
            big = scaled(image, s)
            panel.paste(big, (x, y), big)
            x += image.width * s + pad
        y += image.height * max(scales) + pad
    return panel


def cmd_zoom(args):
    sprites = load_all(args.sprites, args.size)
    cards = []
    for sprite in sprites:
        cell = 14 if sprite.size == 16 else 12
        tile = grid_tile(sprite, cell)
        image = sprite.image()
        grey = Image.merge("RGBA", (*[image.convert("L")] * 3, image.getchannel("A")))
        panels = [size_panel([image], LIGHT), size_panel([image], DARK), size_panel([grey], LIGHT, (2, 3))]
        pw = max(p.width for p in panels)
        card = Image.new("RGB", (tile.width + pw + 14, max(tile.height, sum(p.height + 6 for p in panels)) + 22),
                         (214, 214, 214))
        card.paste(tile, (4, 4))
        y = 4
        for p in panels:
            card.paste(p, (tile.width + 10, y))
            y += p.height + 6
        errors, warnings, _ = lint(sprite)
        tag = ("  ERRORS" if errors else f"  {len(warnings)} warning{'s' if len(warnings) != 1 else ''}" if warnings
               else "  ok")
        ImageDraw.Draw(card).text((6, card.height - 17), sprite.label() + tag, font=font(12),
                                  fill=(170, 0, 0) if errors else (20, 20, 20))
        cards.append(card)
    save_board(cards, args.out, args.cols)


def save_board(cards, out, cols):
    cols = max(1, min(cols, len(cards)))
    rows = [cards[i:i + cols] for i in range(0, len(cards), cols)]
    width = max(sum(c.width + 6 for c in row) for row in rows) + 6
    height = sum(max(c.height for c in row) + 6 for row in rows) + 6
    board = Image.new("RGB", (width, height), (196, 196, 196))
    y = 6
    for row in rows:
        x = 6
        for card in row:
            board.paste(card, (x, y))
            x += card.width + 6
        y += max(c.height for c in row) + 6
    save_image(board, out)


def cmd_sheet(args):
    """Side by side: references, then each sprite big, at 1x and 2x on light and dark, and among neighbours."""
    sprites = load_all(args.sprites, args.size)
    neighbors = load_all(args.neighbor or [], args.size)
    refs = []
    for spec in args.ref or []:
        refs.append((open_image(spec), image_name(spec)))
    for code in args.twemoji or []:
        refs.append((twemoji_image(code, 160), f"Twemoji {code}"))
    for code in args.emoji or []:
        refs.append((system_emoji(code, 160), f"system emoji {code}"))
    big = 192
    head = font(12)
    cards = []
    for image, label in refs:
        card = Image.new("RGB", (big + 12, big + 30), (255, 255, 255))
        shown = fit(image, big, big)
        card.paste(shown, (6 + (big - shown.width) // 2, 6 + (big - shown.height) // 2), shown)
        ImageDraw.Draw(card).text((6, big + 10), label[:30], font=head, fill=(20, 20, 20))
        cards.append(card)
    for sprite in sprites:
        k = big // sprite.size
        image = sprite.image()
        light, dark = size_panel([image], LIGHT, (1, 2, 4)), size_panel([image], DARK, (1, 2, 4))
        width = max(sprite.size * k, light.width) + 12
        card = Image.new("RGB", (width, sprite.size * k + light.height + dark.height + 40), (236, 236, 236))
        b = scaled(image, k)
        card.paste(b, (6, 6), b)
        card.paste(light, (6, sprite.size * k + 12))
        card.paste(dark, (6, sprite.size * k + light.height + 16))
        ImageDraw.Draw(card).text((6, card.height - 18), sprite.label(), font=head, fill=(20, 20, 20))
        cards.append(card)
    strip = []
    for size in sorted({s.size for s in sprites}):
        row = [s.image() for s in neighbors if s.size == size]
        mine = [s.image() for s in sprites if s.size == size]
        mixed = row[:len(row) // 2] + mine + row[len(row) // 2:]
        for background in (LIGHT, DARK):
            for scale in (1, 2):
                strip.append(lineup(mixed, background, scale))
    board_w = max(sum(c.width + 8 for c in cards) + 8, max([s.width for s in strip] or [0]) + 16)
    board_h = max(c.height for c in cards) + 16 + sum(s.height + 4 for s in strip) + 30
    board = Image.new("RGB", (board_w, board_h), (210, 210, 210))
    d = ImageDraw.Draw(board)
    x = 8
    for card in cards:
        board.paste(card, (x, 8))
        x += card.width + 8
    y = max(c.height for c in cards) + 16
    if strip:
        d.text((8, y), "at real size, between neighbours (light and dark, 1x and 2x)", font=head, fill=(20, 20, 20))
        y += 18
        for s in strip:
            board.paste(s, (8, y))
            y += s.height + 4
    save_image(board, args.out)


def lineup(images, background, scale):
    gap = 6 * scale
    width = sum(i.width * scale + gap for i in images) + gap
    height = max(i.height for i in images) * scale + 2 * gap
    row = Image.new("RGB", (width, height), background)
    x = gap
    for image in images:
        big = scaled(image, scale)
        row.paste(big, (x, gap), big)
        x += big.width + gap
    return row


def cmd_render(args):
    sprites = load_all([args.sprite], args.size)
    if len(sprites) != 1:
        raise SpriteError(f"{args.sprite} holds {len(sprites)} sprites; pass --size to pick one")
    save_image(scaled(sprites[0].image(), args.scale), args.out)


BLIND_PROMPT = """\
Open only the images in this folder. Each letter is one tiny icon, shown at real size (LETTER-1x.png), at 2x and
at 4x. For EACH letter, from the pictures alone, answer in a line or two:
1. What is this?
2. What can you tell about the person or subject?
3. Its two most distinctive traits.
4. Possible misreads: what could someone mistake it, or any part of it, for?
Don't guess who anyone is, and don't compare the letters with each other."""

BLIND_RULE = """\
Ask 3 fresh reviewers with no other context: people, or new agents given only the show/ folder and the prompt.
Save every prompt and answer word for word. Before you read the answers, write down what counts as naming each
trait (teeth: 'teeth', 'toothy' or a white mouth, where 'big smile' alone is a different trait; hair: 'dark' or
'black', not 'brown').

A drawing passes a round when 2 of the 3 name its top two traits unprompted: for a person, the first two in its
keep: line, phrased as things a stranger can name at 1x (dark hair, a toothy grin, glasses, a beard); for
anything else, what it is and its key cue. One round is noisy, so pass two rounds running (reshuffled with a new
--seed and new reviewers), or 5 of 9 reads over three rounds. Judge each trait against the controls: once your
drawing scores as well as the approved shape does, stop redrawing.

Ignore any misread that a control gets too. Dark hair on the person-head template reads as a 'helmet', 'hat' or
'beard' even on the approved set:16:1f9d1, so that read is the house style, not your drawing. For a portrait in
a real skin tone, add a skin-matched control: an approved shape with only its skin keys changed to yours.
Reviewer models misread darker skin, even as an animal face; that read follows the skin, not the drawing. Never
change a sampled skin tone because of it. A person makes the respect and likeness call."""


def blind_card(image, k):
    m = image.width * k // 4
    card = Image.new("RGB", (image.width * k + 2 * m, image.height * k + 2 * m), LIGHT)
    big = scaled(image, k)
    card.paste(big, (m, m), big)
    return card


def cmd_blind(args):
    subjects = [(s, "drawing") for s in load_all(args.sprites, args.size)]
    controls = [(s, "control") for s in load_all(args.control, args.size)]
    if len(subjects) + len(controls) > 26:
        raise SpriteError("26 letters at most; split the test")
    out = out_path(args.out)
    show = out / "show"
    old = sorted(show.glob("*-[124]x.png")) if show.is_dir() else []
    if old and not args.force:
        raise SpriteError(f"{show} already holds a blind test; pass --force to replace it, or pick a new --out")
    show.mkdir(parents=True, exist_ok=True)
    for path in old:
        path.unlink()
    seed = args.seed if args.seed is not None else random.randrange(10 ** 6)
    order = subjects + controls
    random.Random(seed).shuffle(order)
    key = [f"Blind test key (seed {seed}). Keep this file from the reviewers; give them only {show}/ and the prompt.",
           ""]
    for letter, (sprite, role) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", order):
        image = sprite.image()
        for k in (1, 2, 4):
            blind_card(image, k).save(show / f"{letter}-{k}x.png")
        key.append(f"{letter}  {role:<8} {sprite.origin} ({sprite.size}px)")
        for field in ("essence", "keep"):
            if sprite.meta.get(field):
                key.append(f"   {field}: {sprite.meta[field]}")
    key += ["", "Prompt:", BLIND_PROMPT, "", "Pass rule:", BLIND_RULE, ""]
    (out / "key.txt").write_text("\n".join(key), encoding="utf-8")
    print(f"{show}/: {len(order)} letters, each at 1x, 2x and 4x on white, with no grid")
    print(f"{out / 'key.txt'}: which letter is which; keep it from the reviewers")
    print()
    print("Prompt (send it word for word, with the show/ images):")
    print(BLIND_PROMPT)
    print()
    print("Pass rule:")
    print(BLIND_RULE)


# ---------------------------------------------------------------- references

def emoji_code(code):
    """'U+1F642', '1F642' and '1f642' all become '1f642'; anything else is returned unchanged."""
    text = re.sub(r"(?i)\bU\+", "", code.strip())
    if re.fullmatch(r"[0-9a-fA-F]{1,6}([- ][0-9a-fA-F]{1,6})*", text):
        parts = re.split(r"[- ]", text.lower())
        for part in parts:
            if int(part, 16) > 0x10FFFF:
                raise SpriteError(f"{code!r}: {part} is not a Unicode code point")
        return "-".join(f"{int(part, 16):x}" if len(part) < 4 else part for part in parts)
    return code


@functools.lru_cache(maxsize=None)
def zip_svgs(path):
    """{name: member} for the .svg files in a zip, at any depth (a release zip keeps them in assets/svg/)."""
    with zipfile.ZipFile(path) as z:
        found = {}
        for member in z.namelist():
            if member.lower().endswith(".svg") and "__MACOSX" not in member:
                found.setdefault(member.rsplit("/", 1)[-1][:-4].lower(), member)
        return found


def local_svg(source, name):
    """NAME.svg from a folder (or its svg/ or assets/svg/) or a zip named in PIXEL_EMOJI_TWEMOJI_DIR."""
    if source.is_dir():
        for sub in ("", "svg", "assets/svg"):
            path = source / sub / f"{name}.svg"
            if path.is_file():
                return path.read_text(encoding="utf-8")
    elif source.is_file() and zipfile.is_zipfile(str(source)):
        member = zip_svgs(str(source)).get(name)
        if member:
            with zipfile.ZipFile(str(source)) as z:
                return z.read(member).decode("utf-8")
    else:
        raise SpriteError(f"{source} (from PIXEL_EMOJI_TWEMOJI_DIR) is not a folder or a zip")
    return None


def twemoji_svg(code):
    """Twemoji's SVG for CODE: from PIXEL_EMOJI_TWEMOJI_DIR, then the cache, then the pinned CDN (then cached)."""
    code = emoji_code(code)
    names = [code] + ([code.replace("-fe0f", "")] if "-fe0f" in code else [])
    for source in env_paths("PIXEL_EMOJI_TWEMOJI_DIR"):
        for name in names:
            svg = local_svg(source, name)
            if svg:
                return svg
    cache = cache_dir() / "twemoji" / f"v{TWEMOJI_VERSION}"
    for name in names:
        if (cache / f"{name}.svg").is_file():
            return (cache / f"{name}.svg").read_text(encoding="utf-8")
    if offline():
        raise SpriteError(f"Twemoji {code}.svg isn't in the cache ({cache}) and downloads are off (--offline or"
                          " PIXEL_EMOJI_OFFLINE). Run it once online, or set PIXEL_EMOJI_TWEMOJI_DIR to a folder or"
                          f" zip of Twemoji SVGs; 'emoji {code}' shows this computer's emoji instead")
    for name in names:
        try:
            data = fetch(CDN.format(name))
        except urllib.error.HTTPError as error:
            if error.code == 404:
                continue
            raise SpriteError(f"the Twemoji CDN answered {error.code} for {name}.svg; try again later, or set"
                              " PIXEL_EMOJI_TWEMOJI_DIR to a folder or zip of Twemoji SVGs")
        except (urllib.error.URLError, OSError) as error:
            raise SpriteError(f"can't reach the Twemoji CDN ({why(error)}) and {code}.svg isn't in the cache. Set"
                              " PIXEL_EMOJI_TWEMOJI_DIR to a folder or zip of Twemoji SVGs, or use"
                              f" 'emoji {code}' for this computer's emoji")
        save_cache(cache / f"{name}.svg", data)
        return data.decode("utf-8")
    raise SpriteError(f"Twemoji has no {code}.svg. Codes are lower-case hex joined by '-', e.g. 1f9d1 or"
                      " 1f468-200d-1f373; most single emoji drop fe0f")


def twemoji_image(code, size):
    svg = twemoji_svg(code)
    try:
        import resvg_py
    except ImportError:
        raise SpriteError("rendering Twemoji needs resvg_py: pip install resvg_py (or use 'emoji CODE' for this"
                          " computer's emoji)")
    png = resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size)
    return Image.open(BytesIO(bytes(png))).convert("RGBA")


def emoji_text(code):
    code = emoji_code(code)
    if re.fullmatch(r"[0-9a-f]{4,6}(-[0-9a-f]{4,6})*", code):
        return "".join(chr(int(part, 16)) for part in code.split("-"))
    return code


def sbix_image(font, name, depth=0):
    """The picture a colour bitmap font stores for glyph NAME in its largest sbix strike."""
    entry, fh = font.reader.tables["sbix"], font.reader.file
    fh.seek(entry.offset)
    count = struct.unpack(">HHI", fh.read(8))[2]
    strikes = []
    for offset in struct.unpack(f">{count}I", fh.read(4 * count)):
        fh.seek(entry.offset + offset)
        strikes.append((struct.unpack(">H", fh.read(2))[0], offset))
    strike = entry.offset + max(strikes)[1]
    fh.seek(strike + 4 + 4 * font.getGlyphID(name))
    start, end = struct.unpack(">II", fh.read(8))
    if end - start <= 8:
        return None
    fh.seek(strike + start)
    kind = fh.read(8)[4:]
    data = fh.read(end - start - 8)
    if kind in (b"dupe", b"flip") and depth < 3:     # another glyph's picture, as is or mirrored
        image = sbix_image(font, font.getGlyphName(struct.unpack(">H", data[:2])[0]), depth + 1)
        return ImageOps.mirror(image) if image is not None and kind == b"flip" else image
    return Image.open(BytesIO(data)).convert("RGBA") if kind == b"png " else None


def apple_emoji(path, text):
    """Apple Color Emoji's own picture of TEXT, or None.

    Pillow without a text shaper (raqm) draws a ZWJ sequence such as man cook as its parts side by side. Apple
    names every ligature glyph after its codepoints (man cook is u1F468_u1F373.0: skin tone .0-.5, gender sign
    .M/.W, facing right .u27A1), so the right picture can be found by name. Families and couples are assembled
    from parts at layout time and have no single glyph."""
    try:
        from fontTools.ttLib import TTCollection, TTFont
    except ImportError:
        return None
    try:
        font = TTCollection(path, lazy=True).fonts[0] if path.lower().endswith(".ttc") else TTFont(path, lazy=True)
    except Exception:
        return None
    try:
        if "sbix" not in font.reader.tables:
            return None
        cps = [ord(c) for c in text if ord(c) not in (0xFE0E, 0xFE0F)]
        tones = "".join(str(c - 0x1F3FA) for c in cps if 0x1F3FB <= c <= 0x1F3FF)
        cps = [c for c in cps if not 0x1F3FB <= c <= 0x1F3FF]
        tail = ""
        if cps[-2:] == [0x200D, 0x27A1]:
            cps, tail = cps[:-2], ".u27A1"
        if cps[-2:] in ([0x200D, 0x2642], [0x200D, 0x2640]):
            tail = (".M" if cps[-1] == 0x2642 else ".W") + tail
            cps = cps[:-2]
        base = "_".join("u%04X" % c for c in cps if c != 0x200D)
        candidates = [f"{base}.{tones}{tail}"] if tones else [f"{base}.0{tail}", f"{base}{tail}", f"{base}.66{tail}"]
        cmap = font.getBestCmap()
        if len(cps) == 1 and not tones and not tail and cps[0] in cmap:
            candidates.insert(0, cmap[cps[0]])
        names = set(font.getGlyphOrder())
        name = next((n for n in candidates if n in names), None)
        return sbix_image(font, name) if name else None
    except (OSError, KeyError, ValueError, struct.error):
        return None
    finally:
        font.close()


def emoji_fonts():
    """(path, the pixel size it loads at) for each colour emoji font: PIXEL_EMOJI_FONT first, then the system's."""
    override = os.environ.get("PIXEL_EMOJI_FONT")
    if override and not Path(override).expanduser().is_file():
        raise SpriteError(f"PIXEL_EMOJI_FONT {override}: no such font file")
    paths = ([str(Path(override).expanduser())] if override else []) + [p for p in EMOJI_FONTS if Path(p).is_file()]
    for path in paths:
        for px in EMOJI_PX:
            try:
                yield path, px, ImageFont.truetype(path, px)
                break
            except OSError:
                continue


def system_emoji(code, size):
    text = emoji_text(code)
    parts = [c for c in text if ord(c) not in (0xFE0E, 0xFE0F)]
    found = []
    for path, px, face in emoji_fonts():
        found.append(Path(path).name)
        glyph = apple_emoji(path, text)
        if glyph is None:
            if len(parts) > 1 and not features.check("raqm"):
                print(f"note: {code} is a sequence this Pillow can't shape (no raqm), so the emoji shows its parts"
                      f" side by side; use the Twemoji original as the reference", file=sys.stderr)
            canvas = Image.new("RGBA", (px * (len(parts) + 2), px * 2), (0, 0, 0, 0))
            try:
                ImageDraw.Draw(canvas).text((px // 2, px // 2), text, font=face, embedded_color=True)
            except (OSError, ValueError):
                continue
            glyph = canvas
        bounds = glyph.getbbox()
        if bounds:
            return fit(glyph.crop(bounds), size, size)
    if found:
        raise SpriteError(f"{', '.join(found)} has no picture for {code}; check the code, or use 'twemoji {code}'")
    raise SpriteError("no colour emoji font found (Apple Color Emoji, Noto Color Emoji or Segoe UI Emoji). Set"
                      f" PIXEL_EMOJI_FONT to a colour emoji font file, or use 'twemoji {code}'")


def cmd_twemoji(args):
    save_image(twemoji_image(args.code, args.size), args.out)


def cmd_emoji(args):
    save_image(system_emoji(args.code, args.size), args.out)


# ---------------------------------------------------------------- photos and colour

def merge_colors(counts, distance, members=None):
    """Greedy clusters of (rgb, count), most common first; returns [(rgb, count)] by count.

    MEMBERS, if given, is filled with {rgb: index of its cluster in the returned list}."""
    clusters, joined = [], {}
    for color, count in counts.most_common():
        for i, c in enumerate(clusters):
            if sum((p - q) ** 2 for p, q in zip(color, c[0])) <= distance ** 2:
                total = c[1] + count
                c[0] = tuple((p * c[1] + q * count) / total for p, q in zip(c[0], color))
                c[1] = total
                break
        else:
            i = len(clusters)
            clusters.append([tuple(float(v) for v in color), count])
        joined[color] = i
    order = sorted(range(len(clusters)), key=lambda i: -clusters[i][1])
    if members is not None:
        rank = {old: new for new, old in enumerate(order)}
        members.update((color, rank[i]) for color, i in joined.items())
    return [(tuple(clusters[i][0]), clusters[i][1]) for i in order]


def opaque_pixels(image):
    px = np.asarray(image).reshape(-1, 4).astype(int)
    px = px[px[:, 3] > 200][:, :3]
    if not len(px):
        raise SpriteError("the box has no opaque pixels")
    return px


def skin_like(px):
    """Warm, coloured pixels: skin of every tone. Greys, black, white, blue and green (most hair, eyes, teeth,
    glasses and backgrounds) fall out; brown or blond hair, lips and orange clothes don't, so box only skin."""
    mx, mn = px.max(1), px.min(1)
    chroma = (mx - mn).astype(float)
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    safe = np.where(chroma > 0, chroma, 1)
    hue = np.where(mx == r, ((g - b) / safe) % 6, np.where(mx == g, (b - r) / safe + 2, (r - g) / safe + 4)) * 60
    sat = np.where(mx > 0, chroma / np.maximum(mx, 1), 0)
    return (chroma > 0) & ((hue <= 50) | (hue >= 335)) & (sat >= 0.08) & (sat <= 0.85) & (mx >= 38)


SKIN_WINDOW = 15   # the base comes from the lit mid-tones: the face average to this much lighter
SKIN_LIMIT = 15    # check --face: a drawing's skin must average within this much of the photo's face


def face_sample(image, distance=28):
    """Skin clusters of a face photo, with the flash or shine, the shadow, the face average and the base."""
    px = opaque_pixels(image)
    skin = px[skin_like(px)]
    if len(skin) < 20 or len(skin) < 0.15 * len(px):
        raise SpriteError(f"only {len(skin) / len(px):.0%} of the box looks like skin; box one clean patch of cheek or"
                          " forehead, with no hair, brows, eyes or lips in it")
    quantised = [tuple(int(v) for v in (p // 8) * 8 + 4) for p in skin]
    members = {}
    clusters = merge_colors(Counter(quantised), distance, members)
    label = np.array([members[q] for q in quantised])
    n = len(skin)
    big = [i for i, (_, count) in enumerate(clusters) if count / n >= 0.01] or [0]
    shine = max(big, key=lambda i: lum(clusters[i][0]) * (1 - hsv(clusters[i][0])[1]))
    shadow = min(big, key=lambda i: lum(clusters[i][0]))
    flags = {i: role for i, role in ((shine, "flash or shine"), (shadow, "shadow")) if i != 0}   # never the commonest
    kept = ~np.isin(label, list(flags))
    average = tuple(skin[kept].mean(0)) if kept.any() else tuple(skin.mean(0))
    a = lum(average)
    left = [i for i in big if i not in flags]
    lit = [i for i in left if 0 <= lum(clusters[i][0]) - a <= SKIN_WINDOW]
    band = (luminance(skin) >= a) & (luminance(skin) <= a + SKIN_WINDOW) & kept
    if lit:
        base, base_note = clusters[lit[0]][0], "the most common cluster left in the lit mid-tones"
        flags[lit[0]] = "base"
    elif band.any():
        base, base_note = tuple(skin[band].mean(0)), "the mean of the lit mid-tones (no cluster centre falls there)"
    else:
        nearest = min(left or big, key=lambda i: abs(lum(clusters[i][0]) - a))
        base, base_note = clusters[nearest][0], "the cluster left nearest the face average"
        flags[nearest] = "base"
    return {"pixels": len(px), "skin": n, "clusters": clusters, "flags": flags, "average": average,
            "base": base, "base_note": base_note}


def cmd_sample(args):
    image = open_image(args.image, args.box)
    w, h = image.info.get("full_size", image.size)
    crop = args.box or (re.fullmatch(r".+@(\d+,\d+,\d+,\d+)", args.image) or [None, None])[1]
    where = f"{args.image} ({w}x{h} image) {'box ' + args.box if args.box else 'cropped' if crop else 'whole image'}"
    if args.face:
        return face_report(args, image, where)
    px = opaque_pixels(image)
    counts = Counter(tuple(int(v) for v in (p // 8) * 8 + 4) for p in px)
    total = len(px)
    print(f"{where}: {total} pixels")
    for color, count in merge_colors(counts, args.distance)[:args.colors]:
        h, s, v = hsv(color)
        print(f"  {rgb_hex(color)}  {count / total:5.1%}  luminance {lum(color):5.1f}  hue {h * 360:3.0f}"
              f"  sat {s:.2f}  val {v:.2f}")
    print("Pick the base from the lit side, not a highlight or the darkest shadow; then build a ramp with:"
          f' {tool_command()} ramp "HEX". For skin, box a clean patch of cheek or forehead and add --face.')


def face_report(args, image, where):
    found = face_sample(image, args.distance)
    clusters, flags, n = found["clusters"], found["flags"], found["skin"]
    print(f"{where}: {found['pixels']} pixels, {n} look like skin ({n / found['pixels']:.0%})")
    if n / found["pixels"] < 0.5:
        print("  note: under half the box is skin-coloured; box one clean patch of cheek or forehead")
    roles = {"flash or shine": "FLASH OR SHINE: the palest, least saturated; never the base",
             "shadow": "SHADOW: the darkest; never the base", "base": "BASE"}
    shown = [i for i in range(len(clusters)) if i < args.colors or i in flags]
    for i in shown:
        color, count = clusters[i]
        print(f"  {rgb_hex(color)}  {count / n:5.1%}  luminance {lum(color):5.1f}  sat {hsv(color)[1]:.2f}"
              f"  {roles.get(flags.get(i), '')}".rstrip())
    average, base = found["average"], found["base"]
    print(f"face average, without the flash and shadow clusters: {rgb_hex(average)}, luminance {lum(average):.1f}")
    print(f"base {rgb_hex(base)}, luminance {lum(base):.1f}: {found['base_note']} (the face average to"
          f" {SKIN_WINDOW} lighter)")
    spec = args.image + (f"@{args.box}" if args.box else "")
    tool = tool_command()
    print(f'next: {tool} ramp "{rgb_hex(base)}" --hue 3 --value 0.09 --up 1 (light S, base s, shadow t, deep'
          f' shadow u), and once it\'s drawn: {tool} check SPRITE --skin "S,s,t,u" --face "{spec}"')
    print("When photos disagree, sample the most evenly lit one, never a flash photo.")


def cmd_crop(args):
    image = open_image(args.image, args.box)
    w, h = image.info.get("full_size", image.size)
    out = scaled(image, args.scale)
    save_image(out, args.out, f"{image.width}x{image.height} box of the {w}x{h} image, at {args.scale}x ="
                              f" {out.width}x{out.height}")


def toward(h, target, amount):
    d = ((target - h + 0.5) % 1.0) - 0.5
    return (h + max(-amount, min(amount, d))) % 1.0


def make_ramp(color, down, up, dv, ds, dh):
    h, s, v = hsv(hex_rgb(color))
    tones = []
    for k in range(-down, up + 1):
        hue = h if s < 0.08 else toward(h, (60 if k > 0 else 240) / 360, abs(k) * dh / 360)
        sat = max(0.0, min(1.0, s - k * ds))
        val = max(0.0, min(1.0, v + k * dv))
        tones.append(rgb_hex(tuple(c * 255 for c in colorsys.hsv_to_rgb(hue, sat, val))))
    return tones


def cmd_ramp(args):
    color = color_arg(args.color, "ramp")
    tones = make_ramp(color, args.down, args.up, args.value, args.saturation, args.hue)
    darker = {1: "shadow", 2: "deep shadow"}
    lighter = {1: "light", 2: "highlight", 3: "glint"}
    for k, tone in zip(range(-args.down, args.up + 1), tones):
        role = ("base" if k == 0 else darker.get(-k, f"shadow {-k}") if k < 0 else lighter.get(k, f"light {k}"))
        flag = "  reads as ink: leave it out" if k and lum(hex_rgb(tone)) < INK_LUM else ""
        print(f"  {tone}  luminance {lum(hex_rgb(tone)):5.1f}  {role}{flag}")
    if lum(hex_rgb(color)) < 80:
        print(f"note: {color} is a dark base. A black or near-black material (hair, a hat, a cat, a tyre) is drawn in"
              f" slate so the #000000 outline still shows: #66717c light, #3a4148 base, #30363c shade, #262b30 deep"
              f" (the person templates' hair keys H h d k). Nothing"
              f" inside the outline goes below luminance {INK_LUM}.")
    print("Shadows turn cooler and richer, highlights warmer and paler. Use 3-4 tones at 16px, 3-5 at 24px.")


def cmd_draft(args):
    """Mode-downsample an image to a crude proportion draft. Redraw it; never trace it."""
    image = open_image(args.image, args.crop)
    n = args.size
    span = args.fit or n - 2
    k = 8
    s = span * k / max(image.size)
    cw, ch = max(1, round(image.width * s / k)), max(1, round(image.height * s / k))
    px = np.asarray(image.resize((cw * k, ch * k), Image.LANCZOS)).astype(int)
    key_rgb = np.array(hex_rgb(color_arg(args.clear, "--clear"))) if args.clear else None
    cells = {}
    for cy in range(ch):
        for cx in range(cw):
            block = px[cy * k:(cy + 1) * k, cx * k:(cx + 1) * k].reshape(-1, 4)
            solid = block[block[:, 3] > 160]
            if key_rgb is not None:
                solid = solid[np.abs(solid[:, :3] - key_rgb).sum(1) > args.tolerance]
            if len(solid) < k * k // 2:
                continue
            counts = Counter(tuple(int(v) for v in (c[:3] // 16) * 16 + 8) for c in solid)
            cells[(cx, cy)] = counts.most_common(1)[0][0]
    if not cells:
        raise SpriteError("nothing left to draft; check --crop and --clear")
    palette = [c for c, _ in merge_colors(Counter(cells.values()), 40)][:args.colors]

    def nearest(color):
        return min(range(len(palette)), key=lambda i: sum((p - q) ** 2 for p, q in zip(color, palette[i])))

    order = sorted(range(len(palette)), key=lambda i: lum(palette[i]))
    key = {i: KEYS[rank] for rank, i in enumerate(order)}
    ox, oy = (n - cw) // 2, (n - ch) // 2
    rows = [["."] * n for _ in range(n)]
    for (cx, cy), color in cells.items():
        if 0 <= cx + ox < n and 0 <= cy + oy < n:
            rows[cy + oy][cx + ox] = key[nearest(color)]
    sprite = Sprite(f"draft of {image_name(args.image)}", ["".join(r) for r in rows],
                    {key[i]: (rgb_hex(palette[i]), "") for i in range(len(palette))},
                    {"essence": "DRAFT -- proportions only. Redraw every pixel by hand; never trace this"})
    if args.out:
        write_text_out(sprite.text(), args.out, args.force)
    else:
        sys.stdout.write(sprite.text())


# ---------------------------------------------------------------- text, export, new

def cmd_text(args):
    text = "\n".join(sprite.text() for sprite in load_all(args.sprites, args.size))
    if args.out:
        write_text_out(text, args.out, args.force)
    else:
        sys.stdout.write(text + "\n")


def cmd_export(args):
    sprite = load_all([args.sprite], args.size)[0]
    name = re.sub(r"[^A-Z0-9]+", "_", args.name.upper()).strip("_")
    if not name or name[0].isdigit():
        raise SpriteError(f"--name {args.name!r}: start with a letter, e.g. TANGERINE16")
    keys = {"#": "#000000", **{k: c for k, (c, _) in sprite.palette.items()}}
    lines = [f"# {sprite.name}, {sprite.size}px: '#' is ink, '.' is clear", f"ROWS_{name} = ["]
    lines += [f'    "{row}",' for row in sprite.rows]
    lines += ["]", f"KEYS_{name} = {{" + ", ".join(f'"{k}": "{c}"' for k, c in keys.items()) + "}"]
    text = "\n".join(lines) + "\n"
    if args.out:
        write_text_out(text, args.out, args.force)
    else:
        sys.stdout.write(text)


def tool_command():
    """How to run this script from the current folder."""
    python = "py" if os.name == "nt" else "python3"
    script = Path(__file__).resolve()
    try:
        here = script.relative_to(Path.cwd().resolve())
    except ValueError:
        return f'{python} "{script}"'
    return f"{python} {here.as_posix()}"


def find_entries(size):
    """The subjects to search at SIZE: the --set-dir and PIXEL_EMOJI_SET_DIR sets first, then the library."""
    seen, out = set(), []
    for source in set_sources():
        for entry in source.entries(size):
            ids = {i for i in (entry["code"], entry["slug"]) if i}
            if ids and not ids & seen:
                seen |= ids
                out.append(dict(entry, where="set"))
    for item in reference_catalog().values():
        if size in item["sizes"] and not {item["code"], item["slug"]} & seen:
            out.append(catalog_entry(item, "ref"))
    return out


def cmd_find(args):
    """Approved sprites whose name, file name, keywords, code or category contain every WORD."""
    entries = find_entries(args.size)
    words = [w.lower() for w in args.words]

    def text(entry):
        keywords = entry["keywords"]
        keywords = " ".join(keywords) if isinstance(keywords, (list, tuple)) else str(keywords)
        return " ".join((entry["name"], entry["slug"], keywords, entry["code"], entry["category"])).lower()

    hits = [entry for entry in entries if all(w in text(entry) for w in words)]
    hits.sort(key=lambda entry: not all(w in entry["name"].lower() for w in words))
    sets = len(set_sources())
    searched = (f"the reference library ({sum(args.size in i['sizes'] for i in reference_catalog().values())}"
                f" subjects at {args.size}px)" + (f" and {sets} set folder{'s' if sets != 1 else ''}" if sets else ""))
    if not hits:
        raise SpriteError(f"nothing in {searched} matches every word of {' '.join(args.words)!r}; try fewer or"
                          f" other words. For the whole Pixel set, download the free PNGs from {FULL_SET} and"
                          " pass the zip or its folder with --set-dir (or PIXEL_EMOJI_SET_DIR)")
    for entry in hits[:args.limit]:
        ident = entry["code"] or entry["slug"]
        print(f"{ident:<22} {entry['slug']:<34} {entry['name']}"
              f"{'  [' + entry['category'] + ']' if entry['category'] else ''}  ({entry['where']})")
    if len(hits) > args.limit:
        print(f"... and {len(hits) - args.limit} more; add a word or raise --limit")
    print(f"(ref = the skill's reference library, set = a --set-dir set.) Study one with:"
          f" {tool_command()} text set:{args.size}:{hits[0]['code'] or hits[0]['slug']}")


def cmd_mirror(args):
    """Copy one half of a sprite onto the other about x + x' = AXIS, so a symmetric shape is exactly symmetric."""
    sprites = load_all([args.sprite], args.size)
    if len(sprites) != 1:
        raise SpriteError(f"{args.sprite} holds {len(sprites)} sprites; pass --size to pick one")
    sprite = sprites[0]
    n = sprite.size
    axis = n - 1 if args.axis is None else args.axis
    if not n // 2 <= axis <= 2 * n - 2 - n // 2:
        raise SpriteError(f"--axis {axis} is far off centre; at {n}px use {n - 2}, {n - 1} or {n}"
                          f" (x + x' = axis: {n - 1} for a {n}-wide subject, {n} for a {n - 1}-wide one on columns 1-{n - 1})")
    swap = {}
    for pair in filter(None, (args.swap or "").split(",")):
        a, sep, b = (part.strip() for part in pair.partition("="))
        if not sep or len(a) != 1 or len(b) != 1:
            raise SpriteError(f"--swap {args.swap!r}: write pairs of keys, e.g. S=t,W=t")
        for key in (a, b):
            if key not in sprite.palette and key not in "#.":
                raise SpriteError(f"--swap: {key!r} is not in [palette]")
        swap[a] = b
    only = args.only
    if only is not None:
        unknown = [key for key in only if key not in sprite.palette and key not in "#."]
        if not only or unknown:
            raise SpriteError(f"--only {only!r}: give keys from [palette], '#' or '.', e.g. --only \"#.\"")
    rows = [list(row) for row in sprite.rows]
    changed = 0
    for y in range(n):
        for x in range(n):
            xr = axis - x
            if 0 <= xr < n and (x < xr if args.keep == "left" else x > xr):
                key = sprite.rows[y][x]
                if only is not None and key not in only and rows[y][xr] not in only:
                    continue   # coloured on both sides: the far side keeps its own tone (its rim light)
                new = swap.get(key, key)
                changed += new != rows[y][xr]
                rows[y][xr] = new
    mirrored = Sprite(sprite.name, ["".join(row) for row in rows], sprite.palette, dict(sprite.meta))
    write_text_out(mirrored.text(), args.out, args.force)
    print(f"{changed} pixel{'s' if changed != 1 else ''} changed", file=sys.stderr)
    other = "right" if args.keep == "left" else "left"
    if not swap and only is None:
        print(f"The {other} half now carries the {args.keep} half's tones. Light comes from the upper left, so"
              f" re-shade the {other} side by hand (or pass --swap LIGHT=SHADE, e.g. --swap S=t).", file=sys.stderr)


def cmd_new(args):
    if args.template:
        path = TEMPLATES / f"{args.template}.sprite"
        if not path.exists():
            names = ", ".join(sorted(p.stem for p in TEMPLATES.glob("*.sprite")))
            raise SpriteError(f"no template {args.template!r}; templates: {names}")
        sprite = parse_sprite(path)
        if args.size and sprite.size != args.size:
            raise SpriteError(f"template {args.template} is {sprite.size}px, not {args.size}px")
        meta = {k: v for k, v in sprite.meta.items() if k not in ("essence", "keep", "drop", "view", "rev", "template",
                                                                   "note")}
        if sprite.meta.get("note"):
            print(f"template {args.template}: {sprite.meta['note']}", file=sys.stderr)
        sprite = Sprite(args.name, sprite.rows, sprite.palette, origin=str(path))
        sprite.meta = {"essence": "", "keep": "", "drop": "", "view": "", "rev": "1", "template": args.template,
                       **meta}
    else:
        n = args.size or 16
        sprite = Sprite(args.name, ["." * n] * n, {}, {"essence": "", "keep": "", "drop": "", "view": "", "rev": "1"})
    text = sprite.text()
    if args.out:
        write_text_out(text, args.out, args.force)
    else:
        sys.stdout.write(text)


def skin_keys(text):
    keys = [k for k in re.split(r"[,\s]+", text) if k]
    if len(keys) == 1 and len(keys[0]) > 1:
        keys = list(keys[0])
    bad = [k for k in keys if len(k) != 1 or k in "#."]
    if not keys or bad:
        raise SpriteError(f"--skin {text!r}: give the skin's palette keys, e.g. S,s,t,u")
    return keys


def skin_match(sprite, keys, face):
    """Compare the pixel-weighted average of the skin KEYS with the photo's face average: (error, note)."""
    missing = [k for k in keys if k not in sprite.palette]
    if missing:
        return (f"--skin {','.join(missing)}: not in this sprite's palette"
                f" ({' '.join(sorted(sprite.palette)) or 'it has none'})"), ""
    counts = {k: sum(row.count(k) for row in sprite.rows) for k in keys}
    empty = [k for k in keys if not counts[k]]
    if empty:
        return f"--skin {','.join(empty)}: no pixels use {'it' if len(empty) == 1 else 'them'}", ""
    total = sum(counts.values())
    mean = tuple(sum(hex_rgb(sprite.palette[k][0])[i] * counts[k] for k in keys) / total for i in range(3))
    mine, theirs = lum(mean), lum(face["average"])
    diff = mine - theirs
    side = "lighter" if diff > 0 else "darker"
    text = (f"skin {rgb_hex(mean)} (luminance {mine:.1f}, {total} pixels of {','.join(keys)}) against the photo's"
            f" face average {rgb_hex(face['average'])} ({theirs:.1f}): {abs(diff):.1f} {side}")
    if abs(diff) > SKIN_LIMIT:
        return (text + f", over the {SKIN_LIMIT} limit. Rebuild the ramp from the base sample --face recommends"
                f" ({rgb_hex(face['base'])}), from a box of clean skin (no brows, eyes or hair); never lighten,"
                " darken or 'correct' a skin tone"), ""
    return "", text + f" (limit {SKIN_LIMIT})"


def cmd_check(args):
    if bool(args.skin) != bool(args.face):
        raise SpriteError("--skin and --face go together: check SPRITE --skin S,s,t,u --face PHOTO@SX0,SY0,SX1,SY1")
    keys = skin_keys(args.skin) if args.skin else None
    face = face_sample(open_image(args.face)) if args.face else None
    failed = 0
    for spec in expand(args.sprites):
        try:
            sprites = load(spec, args.size)
        except SpriteError as error:
            print(f"{spec}: ERROR {error}")
            failed += 1
            continue
        for sprite in sprites:
            errors, warnings, stats = lint(sprite)
            note = ""
            if face:
                problem, note = skin_match(sprite, keys, face)
                errors = errors + [problem] if problem else errors
            failed += bool(errors)
            summary = "  ".join(f"{k} {v}" for k, v in stats.items() if k != "notes")
            print(f"{sprite.origin if sprite.origin != sprite.name else sprite.name} ({sprite.size}px):"
                  f" {'ERRORS' if errors else 'ok'}  {summary}")
            if sprite.meta.get("essence"):
                print(f"   essence: {sprite.meta['essence']}")
            if sprite.status:
                print(f"   ({sprite.status})")
            if note:
                print("   skin ", note)
            for line in errors:
                print("   ERROR", line)
            for line in warnings:
                print("   warn ", line)
            for line in stats.get("notes", []):
                print("   note ", line)
    return 1 if failed else 0


def build_parser():
    """The command-line parser, without running anything (the tests use it to check documented commands)."""
    raw = argparse.RawDescriptionHelpFormatter
    p = argparse.ArgumentParser(description=__doc__, epilog=SOURCES, formatter_class=raw)
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--set-dir", action="append", metavar="DIR",
                        help="a folder or zip of Pixel set PNGs for set: and find, searched before"
                             " PIXEL_EMOJI_SET_DIR and the reference library (repeatable)")
    common.add_argument("--offline", action="store_true",
                        help="never download; use local files and the cache (or set PIXEL_EMOJI_OFFLINE=1)")

    def add(name, func, help_text, more=""):
        q = sub.add_parser(name, help=help_text, description=help_text + ("\n\n" + more if more else ""),
                           epilog=SOURCES if "SPRITE" in more + help_text else None, formatter_class=raw,
                           parents=[common])
        q.set_defaults(func=func)
        return q

    def whole(low):
        def parse(text):
            try:
                value = int(text)
            except ValueError:
                raise argparse.ArgumentTypeError(f"{text!r} is not a whole number")
            if value < low:
                raise argparse.ArgumentTypeError(f"{value} is too small; use {low} or more")
            return value
        return parse

    def sizes(q, what="with MODULE.py: sources, draw only this size (default: every size the module draws)"):
        q.add_argument("--size", type=int, choices=(16, 24), help=what)

    q = add("check", cmd_check, "lint SPRITEs against the house rules (exit 1 on errors)",
            "Errors break the style and must be fixed. Warnings need a look and can be right on purpose:\n"
            "name the reason, or fix it. Lint is a gate, not a quality judgment; judge with zoom and sheet.\n\n"
            "For a portrait in real skin tones, --skin and --face also compare the drawing's skin with the photo:\n"
            "the pixel-weighted average of the skin keys must be within 15 luminance of the face average that\n"
            "sample --face prints for the same box, or check reports an ERROR. Skip it for yellow variants.")
    q.add_argument("sprites", nargs="+", metavar="SPRITE")
    q.add_argument("--skin", metavar="KEYS", help="the skin's palette keys, e.g. S,s,t,u (needs --face)")
    q.add_argument("--face", metavar="PHOTO@SX0,SY0,SX1,SY1",
                   help="the photo and the skin box you ran sample --face on (needs --skin)")
    sizes(q)
    q = add("zoom", cmd_zoom, "judge single pixels: each SPRITE on a big numbered grid with mirror axes,"
            " at 1x-3x on light and dark, and in greyscale")
    q.add_argument("sprites", nargs="+", metavar="SPRITE")
    q.add_argument("--out", required=True, help="the PNG to write")
    q.add_argument("--cols", type=whole(1), default=2, help="cards per row (default 2)")
    sizes(q)
    q = add("sheet", cmd_sheet, "review board: references beside each SPRITE, then the SPRITEs at real size"
            " among --neighbor sprites, on light and dark")
    q.add_argument("sprites", nargs="+", metavar="SPRITE")
    q.add_argument("--out", required=True, help="the PNG to write")
    q.add_argument("--ref", action="append", metavar="IMAGE",
                   help="a photo or picture of the subject; IMAGE@X0,Y0,X1,Y1 crops it, e.g. to the face (repeatable)")
    q.add_argument("--twemoji", action="append", metavar="CODE", help="a Twemoji code to show, e.g. 1f9d1 (repeatable)")
    q.add_argument("--emoji", action="append", metavar="CODE",
                   help="a code like 1f9d1, or the character itself, to show as the system colour emoji (repeatable)")
    q.add_argument("--neighbor", action="append", metavar="SPRITE",
                   help="an approved sprite, e.g. set:16:1f642, to set yours beside (repeatable)")
    sizes(q)
    q = add("render", cmd_render, "write a SPRITE as a PNG with binary alpha")
    q.add_argument("sprite", metavar="SPRITE")
    q.add_argument("--out", required=True, help="the PNG to write")
    q.add_argument("--scale", type=whole(1), default=1, help="whole-number nearest-neighbour scale (default 1)")
    sizes(q)
    q = add("blind", cmd_blind, "a blind test: SPRITEs and approved controls, shuffled under letters, to show"
            " fresh reviewers",
            "Writes OUT/show/LETTER-1x.png, -2x.png and -4x.png (on white, no grid) for every SPRITE and every\n"
            "--control, shuffled, and OUT/key.txt with which letter is which. Give reviewers only OUT/show/ and\n"
            "the prompt it prints. Always include at least one approved neighbour as a control, e.g.\n"
            "--control set:16:1f9d1 for a person.\n\n" + BLIND_RULE)
    q.add_argument("sprites", nargs="+", metavar="SPRITE")
    q.add_argument("--control", action="append", required=True, metavar="SPRITE",
                   help="an approved sprite to shuffle in unlabelled, e.g. set:16:1f9d1 (repeatable; at least one)")
    q.add_argument("--out", required=True, help="the folder to write show/ and key.txt in")
    q.add_argument("--seed", type=int, help="shuffle seed, to repeat a test (default: random; key.txt records it)")
    q.add_argument("--force", action="store_true", help="replace an earlier test in --out")
    sizes(q)
    q = add("text", cmd_text, "print SPRITEs (PNG, set:, MODULE.py:) as .sprite text, to study approved grids",
            "With --out it writes the text to a file instead, e.g. to copy an approved drawing into the work\n"
            "folder and practise the review loop on it.")
    q.add_argument("sprites", nargs="+", metavar="SPRITE")
    q.add_argument("--out", help="a .sprite file to write instead of printing (a bare name goes to the work folder)")
    q.add_argument("--force", action="store_true", help="replace --out if it exists")
    sizes(q)
    q = add("export", cmd_export, "print a SPRITE as ROWS_NAME and KEYS_NAME Python lists",
            "ROWS_NAME is the grid as strings of one-character keys and KEYS_NAME maps each key to #rrggbb\n"
            "('#' is ink, '.' is clear). Paste them into a Python module; MODULE.py:NAME reads them back, and\n"
            "your own code can draw them. A project that keeps its art in Python registers them its own way.")
    q.add_argument("sprite", metavar="SPRITE")
    q.add_argument("--name", required=True, help="the Python name, e.g. TANGERINE16 for ROWS_TANGERINE16")
    q.add_argument("--out", help="a .py file to write instead of printing (a bare name goes to the work folder)")
    q.add_argument("--force", action="store_true", help="replace --out if it exists")
    sizes(q)
    q = add("new", cmd_new, "start a .sprite file, blank or from a template",
            "Templates live in templates/ in the skill folder: " +
            ", ".join(sorted(t.stem for t in TEMPLATES.glob("*.sprite"))) + ".")
    q.add_argument("name", help="the subject, e.g. tangerine")
    q.add_argument("--size", type=int, choices=(16, 24), help="16 or 24 (default 16, or the template's size)")
    q.add_argument("--template", help="a template name, e.g. smiley-head-16")
    q.add_argument("--out", help="the .sprite file to write (default: print it; a bare name goes to the work folder)")
    q.add_argument("--force", action="store_true", help="replace --out if it exists")
    q = add("mirror", cmd_mirror, "copy one half of a SPRITE onto the other, so a symmetric shape is exact",
            "Draw the left half of a symmetric subject (a face, a skull, a bottle), then mirror it. Each pixel x\n"
            "is copied to x' = AXIS - x. AXIS is 15 (16px) or 23 (24px) for a subject that is an even number of\n"
            "pixels wide and centred, and 16 or 24 for an odd-width one whose middle column is 8 or 12 (the 15px\n"
            "smiley head on columns 1-15). check reports the axis a drawing is closest to. Light comes from the\n"
            "upper left, so the copied half carries the wrong tones: re-shade it, or --swap them as you copy.\n"
            "On a lit head or body that is already shaded (any template), pass --only \"#.\": it copies the ink\n"
            "and the silhouette (eyes, mouth, glasses, the outline) and leaves every pixel that is coloured on\n"
            "both sides alone, so the far rim keeps its shade tones.")
    q.add_argument("sprite", metavar="SPRITE")
    q.add_argument("--out", required=True, help="the .sprite file to write (a new rev file)")
    q.add_argument("--axis", type=int, help="x + x' for mirrored columns (default: size - 1)")
    q.add_argument("--keep", choices=("left", "right"), default="left", help="the half to copy from (default left)")
    q.add_argument("--swap", metavar="A=B,...", help="keys to change in the copy, e.g. S=t,W=t (light to shade)")
    q.add_argument("--only", metavar="KEYS", help='copy a pixel only where either side is one of KEYS, e.g. "#."'
                   " (ink and clear): fixes features and outline, keeps the far side's shading")
    q.add_argument("--force", action="store_true", help="replace --out if it exists")
    sizes(q)
    q = add("find", cmd_find, "approved sprites to study: code, file name and name for WORDs",
            "Searches the skill's reference library (about 250 subjects at both sizes) and any --set-dir set:\n"
            "names, file names, keywords, codes and categories. Every WORD must match (part of a word counts,\n"
            "so 'smil' finds smile and smiling). With no WORD it lists everything, up to --limit.\n"
            "Study what it finds with text set:SIZE:CODE, or set it beside your drawing with sheet --neighbor.")
    q.add_argument("words", nargs="*", metavar="WORD")
    q.add_argument("--size", type=int, choices=(16, 24), default=16, help="16 or 24 (default 16)")
    q.add_argument("--limit", type=whole(1), default=20, help="most results to list (default 20)")
    q = add("draft", cmd_draft, "a crude proportion draft of any image (redraw it; never trace it)",
            "Mode-downsamples the image so you can see where the big masses sit on the grid. The result is\n"
            "mush: use it to plan proportions, then draw every pixel yourself.")
    q.add_argument("image", metavar="IMAGE")
    q.add_argument("--size", type=int, choices=(16, 24), default=16, help="16 or 24 (default 16)")
    q.add_argument("--crop", metavar="X0,Y0,X1,Y1", help="crop the image first, in image pixels")
    q.add_argument("--fit", type=whole(4), help="pixels on the long side (default size - 2)")
    q.add_argument("--colors", type=whole(1), default=8, help="most colours to keep (default 8)")
    q.add_argument("--clear", metavar="HEX", help="a background colour to drop, e.g. #9a9a9a")
    q.add_argument("--tolerance", type=whole(0), default=60, help="how far from --clear still counts as background")
    q.add_argument("--out", help="a .sprite file to write instead of printing (a bare name goes to the work folder)")
    q.add_argument("--force", action="store_true", help="replace --out if it exists")
    q = add("sample", cmd_sample, "dominant colours inside a box of a photo (skin, hair, clothes)",
            "With --face, it keeps only skin-coloured pixels (greys, black, white, blue and green fall out, but\n"
            "brown or blond hair, lips and orange clothes don't). Box one clean patch: the cheeks and nose between\n"
            "the eyes and the mouth, or the forehead; brows and eyes in the box drag the average darker. It lists the\n"
            "skin clusters with their share, luminance and saturation, flags the palest least-saturated cluster\n"
            "(flash or shine) and the darkest (shadow), averages the face without them, and recommends the base:\n"
            "the most common cluster left in the lit mid-tones, from the face average to 15 lighter (or, if no\n"
            "cluster centre falls there, their mean). When photos disagree, sample the most evenly lit one, never\n"
            "a flash photo.")
    q.add_argument("image", metavar="IMAGE", help="a picture; IMAGE@X0,Y0,X1,Y1 boxes it, like --box")
    q.add_argument("--box", metavar="X0,Y0,X1,Y1", help="the area to sample, in image pixels (default: all)")
    q.add_argument("--face", action="store_true", help="sample skin: flag flash and shadow, recommend the base")
    q.add_argument("--colors", type=whole(1), default=6, help="how many colours to list (default 6)")
    q.add_argument("--distance", type=whole(0), default=28, help="RGB distance that merges similar colours (default 28)")
    q = add("crop", cmd_crop, "cut a box out of a photo and enlarge it, to check the box before you sample or draw")
    q.add_argument("image", metavar="IMAGE", help="a picture; IMAGE@X0,Y0,X1,Y1 boxes it, like --box")
    q.add_argument("--box", metavar="X0,Y0,X1,Y1", help="the area to keep, in image pixels (default: all)")
    q.add_argument("--scale", type=whole(1), default=1, help="whole-number nearest-neighbour scale (default 1)")
    q.add_argument("--out", required=True, help="the PNG to write")
    q = add("ramp", cmd_ramp, "a hue-shifted tone ramp around a base colour")
    q.add_argument("color", metavar="HEX", help="the base colour, e.g. #f4900c")
    q.add_argument("--down", type=whole(0), default=2, help="shadow tones (default 2)")
    q.add_argument("--up", type=whole(0), default=2, help="light tones (default 2)")
    q.add_argument("--value", type=float, default=0.13, help="HSV value step per tone (default 0.13)")
    q.add_argument("--saturation", type=float, default=0.07, help="saturation step per tone (default 0.07)")
    q.add_argument("--hue", type=float, default=7, help="degrees of hue shift per tone (default 7)")
    q = add("twemoji", cmd_twemoji, "render the Twemoji original (needs resvg_py)",
            "Reads CODE.svg from PIXEL_EMOJI_TWEMOJI_DIR (folders or zips of Twemoji SVGs), then the cache,\n"
            f"then the pinned CDN (jdecked/twemoji v{TWEMOJI_VERSION}), which it caches. With --offline it never\n"
            "downloads. Twemoji graphics: Copyright Twitter, Inc. and other contributors, CC BY 4.0.")
    q.add_argument("code", metavar="CODE", help="a Twemoji code, e.g. 1f9d1")
    q.add_argument("--out", required=True, help="the PNG to write")
    q.add_argument("--size", type=whole(16), default=160, help="pixels (default 160)")
    q = add("emoji", cmd_emoji, "render this computer's colour emoji (Apple, Noto or Segoe)",
            "Uses PIXEL_EMOJI_FONT if set, else Apple Color Emoji (macOS), Noto Color Emoji (Linux) or\n"
            "Segoe UI Emoji (Windows).")
    q.add_argument("code", metavar="CODE", help="a code like 1f9d1 or 1f468-200d-1f373, or the character itself")
    q.add_argument("--out", required=True, help="the PNG to write")
    q.add_argument("--size", type=whole(16), default=160, help="pixels on the long side (default 160)")
    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")   # a Windows console can't print every emoji name
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    OPTIONS.set_dirs = tuple(getattr(args, "set_dir", None) or ())
    OPTIONS.offline = bool(getattr(args, "offline", False))
    try:
        return args.func(args) or 0
    except SpriteError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
