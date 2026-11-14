#!/usr/bin/env python3
"""Builds the online theme files for Lumi Exit.

Reads themes.json and raw/<id>.jpg|png, then writes:
  bg/<id>.jpg      full background (768x1376) downloaded when a player buys the theme
  thumb/<id>.jpg   small preview shown in the theme shop
  catalog.json     the list the game downloads

Add a theme: put its image in raw/, add {"id", "name", "price", "hue"} to themes.json,
run `python3 build.py`, then commit and push. Ids must be lowercase letters, digits or _.
"""
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
BG_SIZE = (768, 1376)
THUMB_SIZE = (360, 570)


def cover(image, size):
    """Scales and center-crops image to exactly fill size."""
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def find_source(theme_id):
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = os.path.join(ROOT, "raw", f"{theme_id}.{ext}")
        if os.path.exists(path):
            return path
    return None


def main():
    themes = json.load(open(os.path.join(ROOT, "themes.json")))["themes"]
    os.makedirs(os.path.join(ROOT, "bg"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "thumb"), exist_ok=True)
    seen, catalog, problems = set(), [], []
    for theme in themes:
        theme_id = theme["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_]*", theme_id) or theme_id in seen or theme_id == "aurora":
            problems.append(f"bad or duplicate id: {theme_id!r}")
            continue
        seen.add(theme_id)
        source = find_source(theme_id)
        if source is None:
            problems.append(f"missing raw image for {theme_id}")
            continue
        image = Image.open(source).convert("RGB")
        cover(image, BG_SIZE).save(os.path.join(ROOT, "bg", f"{theme_id}.jpg"), quality=82, optimize=True, progressive=False)
        cover(image, THUMB_SIZE).save(os.path.join(ROOT, "thumb", f"{theme_id}.jpg"), quality=78, optimize=True, progressive=False)
        catalog.append({
            "id": theme_id,
            "name": theme["name"],
            "price": int(theme["price"]),
            "hue": float(theme.get("hue", 0)),
            "bg": f"bg/{theme_id}.jpg",
            "thumb": f"thumb/{theme_id}.jpg",
        })
    catalog.sort(key=lambda entry: (entry["price"], entry["name"]))
    with open(os.path.join(ROOT, "catalog.json"), "w") as file:
        json.dump({"version": 1, "themes": catalog}, file, indent=1)
    print(f"{len(catalog)} themes written to catalog.json")
    for problem in problems:
        print("WARNING:", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
