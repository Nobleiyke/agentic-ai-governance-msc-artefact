from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"


def _register_fonts() -> None:
    """
    Try to register a Unicode-capable font if present.
    Falls back to default PDF fonts if unavailable.
    """
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\calibri.ttf"),
        Path(r"C:\Windows\Fonts\times.ttf"),
    ]
    for p in candidates:
        if p.exists():
            try:
                pdfmetrics.registerFont(TTFont("BodyFont", str(p)))
                return
            except Exception:
                pass


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    _register_fonts()
    body_font = "BodyFont" if "BodyFont" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
    mono_font = "Courier"

    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    width, height = LETTER

    left = 0.85 * inch
    right = 0.85 * inch
    top = 0.85 * inch
    bottom = 0.85 * inch

    y = height - top

    def new_page():
        nonlocal y
        c.showPage()
        y = height - top

    def draw_text(line: str, size: int = 11, bold: bool = False, mono: bool = False, indent: float = 0.0):
        nonlocal y
        if y < bottom + size * 1.6:
            new_page()
        font = mono_font if mono else body_font
        c.setFont(font, size)
        x = left + indent
        c.drawString(x, y, line)
        y -= size * 1.35

    def draw_spacer(px: float = 10.0):
        nonlocal y
        y -= px
        if y < bottom:
            new_page()

    def draw_image(img_path: Path):
        nonlocal y
        if not img_path.exists():
            draw_text(f"[Missing image: {img_path.name}]", size=10)
            return

        # Max width/height for image block.
        max_w = width - left - right
        max_h = 4.6 * inch

        img = ImageReader(str(img_path))
        iw, ih = img.getSize()
        scale = min(max_w / iw, max_h / ih, 1.0)
        w = iw * scale
        h = ih * scale

        # If image would cross bottom margin, start new page first.
        if y - h < bottom:
            new_page()

        x = left
        c.drawImage(img, x, y - h, width=w, height=h, preserveAspectRatio=True, mask="auto")
        y -= h + 14

    md = md_path.read_text(encoding="utf-8", errors="replace").splitlines()

    img_re = re.compile(r"!\[\]\((.+?)\)")
    code_tick_re = re.compile(r"`([^`]+)`")

    for raw in md:
        line = raw.rstrip("\n").rstrip()

        # Ignore horizontal rules
        if line.strip() in {"---", "***", "___"}:
            draw_spacer(8)
            continue

        # Images like ![](./file.png)
        m = img_re.search(line.strip())
        if m:
            ref = m.group(1).strip()
            # Resolve relative to the markdown file directory
            img_path = (md_path.parent / ref).resolve()
            draw_image(img_path)
            continue

        # Headings
        if line.startswith("# "):
            draw_text(line[2:].strip(), size=18)
            draw_spacer(6)
            continue
        if line.startswith("## "):
            draw_text(line[3:].strip(), size=14)
            draw_spacer(4)
            continue
        if line.startswith("### "):
            draw_text(line[4:].strip(), size=12)
            draw_spacer(2)
            continue

        # Bullets
        if line.startswith("- "):
            txt = line[2:].strip()
            # Keep inline code as monospace-ish by surrounding with quotes.
            txt = code_tick_re.sub(r"'\1'", txt)
            draw_text("• " + txt, size=11, indent=10)
            continue

        # Empty line
        if line.strip() == "":
            draw_spacer(8)
            continue

        # Normal paragraph line
        txt = code_tick_re.sub(r"'\1'", line)
        # Very naive wrapping: split long lines to fit page width.
        # This keeps the script dependency-free (no Platypus).
        max_chars = 110
        while len(txt) > max_chars:
            cut = txt.rfind(" ", 0, max_chars)
            if cut <= 0:
                cut = max_chars
            draw_text(txt[:cut].strip(), size=11)
            txt = txt[cut:].strip()
        draw_text(txt, size=11)

    c.save()


def main() -> None:
    md_path = OUT_DIR / "AGENTIC_DATASET_RESULTS_LAY_CONVERTER_SAFE.md"
    pdf_path = OUT_DIR / "AGENTIC_DATASET_RESULTS_LAY.pdf"
    md_to_pdf(md_path, pdf_path)
    print(f"Wrote: {pdf_path}")


if __name__ == "__main__":
    main()

