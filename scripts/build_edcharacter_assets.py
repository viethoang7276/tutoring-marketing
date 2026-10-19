#!/usr/bin/env python3
"""Export the existing EdCharacter SVGs unchanged. Requires CairoSVG and Pillow."""
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/renders/edcharacters"
CAST = (
    ("ledger", "Ledger"),
    ("sigma", "Sigma"),
    ("centi", "Centi"),
    ("plot", "Plot"),
    ("tempo", "Tempo"),
    ("ledger-stuck", "Ledger · stuck"),
)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1440, 1280), "#FFFFFF")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
    except OSError:
        font = ImageFont.load_default()
    for index, (stem, label) in enumerate(CAST):
        path = OUTPUT / (stem + ".png")
        cairosvg.svg2png(
            url=str(ROOT / "assets/brand" / (stem + ".svg")),
            write_to=str(path),
            output_width=960,
            output_height=1080,
        )
        with Image.open(path) as source:
            assert source.mode == "RGBA", "Character exports must retain transparency"
            assert source.getpixel((0, 0))[3] == 0, "Background must stay transparent"
            thumbnail = source.resize((432, 486), Image.Resampling.LANCZOS)
        left, top = (index % 3) * 480, (index // 3) * 640
        sheet.paste(thumbnail, (left + 24, top + 32), thumbnail)
        draw.text((left + 240, top + 560), label, fill="#020817", font=font, anchor="mm")
    sheet.save(OUTPUT / "contact-sheet.png")
    print("Exported six transparent characters and contact-sheet.png to " + str(OUTPUT))


if __name__ == "__main__":
    main()
