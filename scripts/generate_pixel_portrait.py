"""Convert assets/profile.png into an animated row-by-row dot-matrix SVG portrait."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "profile.png"
OUTPUT = ROOT / "assets" / "portrait.svg"
GRID_SIZE = 80
CANVAS_SIZE = 960
CELL_SIZE = CANVAS_SIZE / GRID_SIZE
BACKGROUND = "#0D1117"
REVEAL_DELAY = 0.025


def center_square(image: Image.Image) -> Image.Image:
    """Crop an image to a centered square, preserving the focal middle area."""
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def dot_radius(red: int, green: int, blue: int) -> float:
    """Scale each dot from dark/small to bright/large using source brightness."""
    brightness = (red + green + blue) / (3 * 255)
    return CELL_SIZE * (0.13 + 0.34 * brightness)


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Upload a portrait image at {SOURCE}")

    portrait = center_square(Image.open(SOURCE).convert("RGB")).resize(
        (GRID_SIZE, GRID_SIZE), Image.Resampling.LANCZOS
    )
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 960" role="img" aria-labelledby="title desc">',
        '  <title id="title">Pixel portrait of Sahil Jain</title>',
        '  <desc id="desc">A dot-matrix portrait that reveals one row at a time.</desc>',
        "  <style>",
        "    @keyframes rv{from{opacity:0}to{opacity:1}}",
        "    .rw{animation:rv 0.45s ease-out both}",
    ]
    lines.extend(
        f"    .r{row}{{animation-delay:{row * REVEAL_DELAY:.3f}s}}"
        for row in range(GRID_SIZE)
    )
    lines.extend(
        [
            "  </style>",
            f'  <rect width="960" height="960" rx="480" fill="{BACKGROUND}"/>',
        ]
    )

    center = CANVAS_SIZE / 2
    outer_radius = CANVAS_SIZE / 2 - CELL_SIZE
    for row in range(GRID_SIZE):
        lines.append(f'  <g class="rw r{row}">')
        for column in range(GRID_SIZE):
            x = column * CELL_SIZE + CELL_SIZE / 2
            y = row * CELL_SIZE + CELL_SIZE / 2
            if (x - center) ** 2 + (y - center) ** 2 > outer_radius**2:
                continue
            red, green, blue = portrait.getpixel((column, row))
            radius = dot_radius(red, green, blue)
            lines.append(
                f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" '
                f'fill="#{red:02x}{green:02x}{blue:02x}"/>'
            )
        lines.append("  </g>")
    lines.append("</svg>")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
