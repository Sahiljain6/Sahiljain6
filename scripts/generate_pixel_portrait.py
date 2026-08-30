"""Turn assets/profile.png into a circular dark-theme pixel portrait."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "profile.png"
OUTPUT = ROOT / "assets" / "profile-pixel.png"
GRID_SIZE = 48
CELL_SIZE = 20
BACKGROUND = "#0D1117"


def center_square(image: Image.Image) -> Image.Image:
    """Crop an image to a centered square, preserving the focal middle area."""
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Upload a portrait image at {SOURCE}")

    portrait = center_square(Image.open(SOURCE).convert("RGB")).resize(
        (GRID_SIZE, GRID_SIZE), Image.Resampling.LANCZOS
    )
    size = GRID_SIZE * CELL_SIZE
    canvas = Image.new("RGB", (size, size), BACKGROUND)
    dots = ImageDraw.Draw(canvas)
    radius = int(CELL_SIZE * 0.42)
    center = size / 2
    outer_radius = size / 2 - CELL_SIZE

    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            x = column * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            if (x - center) ** 2 + (y - center) ** 2 > outer_radius**2:
                continue
            color = portrait.getpixel((column, row))
            dots.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, optimize=True)


if __name__ == "__main__":
    main()
