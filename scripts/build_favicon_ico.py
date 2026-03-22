#!/usr/bin/env python3
"""Rasterize DM logo to multi-size favicon.ico (requires Pillow)."""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow: pip install Pillow")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "favicon.ico"

NAVY = (17, 24, 39, 255)
MAROON = (139, 26, 46, 255)
WHITE = (255, 255, 255, 255)


def draw_logo(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = max(2, int(size * 0.22))
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=NAVY)
    # Top-right maroon triangle (matches CSS corner accent)
    tri = [(size - 1, 0), (size - 1, int(size * 0.42)), (int(size * 0.56), 0)]
    draw.polygon(tri, fill=MAROON)
    # "DM" text
    try:
        # Windows
        font = ImageFont.truetype("segoeui.ttf", int(size * 0.38))
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", int(size * 0.38))
        except OSError:
            font = ImageFont.load_default()
    text = "DM"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2 - int(size * 0.06)
    draw.text((x, y), text, font=font, fill=WHITE)
    return img


def main() -> None:
    sizes = (16, 32, 48)
    images = [draw_logo(s) for s in sizes]
    images[0].save(
        OUT,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
