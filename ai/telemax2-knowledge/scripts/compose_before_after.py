#!/usr/bin/env python3
"""Puts e2e "before" and "after" screenshots side by side in one labelled image, one per ticket.

Usage:
  compose_before_after.py OUT.png BEFORE.png AFTER.png [BEFORE2.png AFTER2.png ...]
      [--title "TLM-1234: what the case checks"] [--caption "Expected: ..."] [--caption "Before: ..."] ...
      [--before-label TEXT] [--after-label TEXT]

Each before/after pair becomes one row (before left, after right); several pairs stack top to bottom (e.g. the
Alert and the Fleet Alert report of one bug). The title and captions go in a band above, so the image says which
case it shows. When a screenshot has a sidecar `<name>.box.json` — a list of {"x", "y", "w", "h", "label"?} in that
screenshot's pixels, written from Playwright's locator.boundingBox() — each box is drawn on it: red on before,
green on after, to point at what changed. The result is scaled down to at most 2400 px wide so it uploads to
ClickUp as one attachment. See ai/telemax2-knowledge/06-e2e-before-after-evidence.md.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 2400
GAP = 20
LABEL_HEIGHT = 60
BOX_WIDTH = 5
BEFORE_COLOUR = (200, 30, 30)
AFTER_COLOUR = (20, 130, 60)


def _font(size, bold=True):
    names = ("Arial Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Arial.ttf", "DejaVuSans.ttf")
    for folder in ("/System/Library/Fonts/Supplemental/", "/usr/share/fonts/truetype/dejavu/"):
        for name in names:
            try:
                return ImageFont.truetype(folder + name, size)
            except OSError:
                continue
    return ImageFont.load_default()


def load_boxes(image_path):
    """Returns the boxes of a screenshot's sidecar `<name>.box.json`, or none when it has no sidecar."""
    sidecar = os.path.splitext(image_path)[0] + ".box.json"
    if not os.path.exists(sidecar):
        return []
    with open(sidecar, encoding="utf-8") as f:
        return json.load(f)


def draw_boxes(image, boxes, colour):
    """Draws each {x, y, w, h, label?} box on a copy of the image, the label above the box."""
    image = image.convert("RGB").copy()
    draw = ImageDraw.Draw(image)
    font = _font(22)
    for box in boxes:
        x, y, w, h = (round(box[k]) for k in ("x", "y", "w", "h"))
        pad = BOX_WIDTH + 2
        draw.rectangle([x - pad, y - pad, x + w + pad, y + h + pad], outline=colour, width=BOX_WIDTH)
        if box.get("label"):
            ty = max(0, y - pad - 30)
            tw = draw.textlength(box["label"], font=font)
            draw.rectangle([x - pad, ty, x - pad + tw + 12, ty + 28], fill=colour)
            draw.text((x - pad + 6, ty + 2), box["label"], fill="white", font=font)
    return image


def _header(width, title, captions):
    """The band above the images: the title, then one line per caption."""
    title_font, caption_font = _font(36), _font(26, bold=False)
    lines = ([(title, title_font, (16, 24, 40))] if title else []) + [(c, caption_font, (52, 64, 84)) for c in captions]
    if not lines:
        return None
    height = 20 + sum(48 if f is title_font else 38 for _, f, _ in lines) + 10
    band = Image.new("RGB", (width, height), (242, 247, 255))
    draw = ImageDraw.Draw(band)
    y = 20
    for text, font, colour in lines:
        draw.text((20, y), text, fill=colour, font=font)
        y += 48 if font is title_font else 38
    return band


def compose(pairs, before_label, after_label, title=None, captions=(), boxes=None):
    """Returns one image: an optional title band, then a labelled row per (before, after) pair of PIL images.
    `boxes` holds, per pair, the (before boxes, after boxes) to draw."""
    font = _font(34)
    rows = []
    for i, (before, after) in enumerate(pairs):
        before_boxes, after_boxes = boxes[i] if boxes else ([], [])
        before = draw_boxes(before, before_boxes, BEFORE_COLOUR)
        after = draw_boxes(after, after_boxes, AFTER_COLOUR)
        row = Image.new("RGB", (before.width + GAP + after.width, max(before.height, after.height) + LABEL_HEIGHT), "white")
        draw = ImageDraw.Draw(row)
        draw.text((10, 12), before_label, fill=BEFORE_COLOUR, font=font)
        draw.text((before.width + GAP + 10, 12), after_label, fill=AFTER_COLOUR, font=font)
        row.paste(before, (0, LABEL_HEIGHT))
        row.paste(after, (before.width + GAP, LABEL_HEIGHT))
        rows.append(row)

    width = max(r.width for r in rows)
    band = _header(width, title, list(captions))
    parts = ([band] if band else []) + rows
    image = Image.new("RGB", (width, sum(p.height for p in parts) + GAP * (len(parts) - 1)), "white")
    y = 0
    for part in parts:
        image.paste(part, (0, y))
        y += part.height + GAP

    if image.width > MAX_WIDTH:
        image = image.resize((MAX_WIDTH, round(image.height * MAX_WIDTH / image.width)), Image.LANCZOS)
    return image


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out")
    parser.add_argument("images", nargs="+", help="before/after pairs, before first")
    parser.add_argument("--title", help="the ticket and the case, e.g. 'TLM-3891: Days included hidden for Today'")
    parser.add_argument("--caption", action="append", default=[], help="a line under the title (repeatable)")
    parser.add_argument("--before-label", default="BEFORE (staging, current build)")
    parser.add_argument("--after-label", default="AFTER (local, fix branch)")
    args = parser.parse_args(argv)
    if len(args.images) % 2:
        parser.error("images come in before/after pairs")

    paths = [(args.images[i], args.images[i + 1]) for i in range(0, len(args.images), 2)]
    pairs = [(Image.open(b), Image.open(a)) for b, a in paths]
    boxes = [(load_boxes(b), load_boxes(a)) for b, a in paths]
    compose(pairs, args.before_label, args.after_label, args.title, args.caption, boxes).save(args.out, optimize=True)
    print(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
