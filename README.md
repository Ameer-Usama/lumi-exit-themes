# Lumi Exit themes

Online themes for Lumi Exit. The game downloads `catalog.json` and the small previews in
`thumb/` when the theme shop opens. A full background in `bg/` is downloaded only when a
player buys that theme, so the app stays small and new themes need no app update.

## Add a theme

1. Put a portrait image (9:16, at least 768x1376) at `raw/<id>.jpg`.
   Keep the middle dark and calm: the puzzle board sits on top of it.
2. Add an entry to `themes.json`:
   `{"id": "<id>", "name": "Shown Name", "price": 300, "hue": 120}`
   - `id`: lowercase letters, digits or `_`, never changed once published.
   - `hue`: 0-360 degrees, shifts the arrow and gate colors to match the background.
3. Run `python3 build.py` (needs Pillow). It writes `bg/`, `thumb/` and `catalog.json`.
4. Commit and push. Players see the new theme the next time they open the shop.

Never delete or rename a published theme: players who bought it need its files.
`raw/` stays on your computer and is not uploaded.
