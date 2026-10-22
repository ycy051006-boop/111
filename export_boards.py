"""Export the three standalone exhibition boards from the presentation PDF."""

from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "quanzhou_puppet_preview.pdf"
OUTPUT = ROOT / "quanzhou_exhibition_boards.pdf"
BOARD_DIR = ROOT / "boards"

LABELS = [
    ("掌中有戏，指尖传情", "01_culture_board.png"),
    ("一眼识五角", "02_character_board.png"),
    ("从舞台到日常", "03_products_board.png"),
]


def main() -> None:
    source = fitz.open(SOURCE)
    mm = 72 / 25.4
    bleed = 3 * mm
    trim_width = 900 * mm
    trim_height = 506.25 * mm
    output = fitz.open()
    BOARD_DIR.mkdir(exist_ok=True)

    for label, filename in LABELS:
        matches = [i for i, page in enumerate(source) if label in page.get_text()]
        if len(matches) != 1:
            raise ValueError(f"Expected one board titled {label!r}, found {len(matches)}")
        source_page = source[matches[0]]
        page = output.new_page(
            width=trim_width + 2 * bleed,
            height=trim_height + 2 * bleed,
        )
        page.draw_rect(page.rect, color=None, fill=(8 / 255, 9 / 255, 13 / 255))
        trim = fitz.Rect(bleed, bleed, bleed + trim_width, bleed + trim_height)
        page.show_pdf_page(trim, source, matches[0], keep_proportion=False)
        page.set_trimbox(trim)
        source_page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(
            BOARD_DIR / filename
        )

    output.save(OUTPUT, garbage=4, deflate=True)
    print(f"Exported {len(output)} boards to {OUTPUT}")


if __name__ == "__main__":
    main()
