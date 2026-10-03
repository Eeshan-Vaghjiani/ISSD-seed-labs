"""Create presentation crops from original evidence; retain all terminal output."""
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "Member5" / "evidence"
CROPS = [
    ("S06-task2a-timing-20261003-051013.png", "S06-task2a-timing-cropped.png", (72, 28, 1920, 480)),
    ("S07-task2a-result-20261003-051108.png", "S07-task2a-result-cropped.png", (72, 28, 1920, 610)),
]


def main():
    for source, target, box in CROPS:
        with Image.open(ROOT / "evidence" / source) as image:
            if image.size != (1920, 955):
                raise ValueError(f"Unexpected dimensions for {source}: {image.size}")
            image.crop(box).save(DEST / target)
        with Image.open(DEST / target) as result:
            result.verify()
        print(f"Created {target}")


if __name__ == "__main__":
    main()
