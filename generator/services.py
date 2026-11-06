import csv
import io
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def read_participants(uploaded_file):
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "name" not in [h.strip().lower() for h in reader.fieldnames]:
        raise ValueError("CSV must contain a column named 'name'.")
    # Normalize header names without changing the participant values.
    rows = []
    for row in reader:
        normalized = {(key or "").strip().lower(): (value or "").strip()
                      for key, value in row.items()}
        if normalized.get("name"):
            rows.append(normalized)
    if not rows:
        raise ValueError("No participant rows with a name were found.")
    return rows


def parse_extra_fields(raw):
    fields = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 5:
            raise ValueError(f"Extra field line {line_number}: expected column|x|y|font_size|#color.")
        column, x, y, size, color = parts
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError(f"Extra field line {line_number}: invalid hex color.")
        try:
            fields.append((column.lower(), int(x), int(y), int(size), color))
        except ValueError:
            raise ValueError(f"Extra field line {line_number}: x, y and font size must be numbers.")
    return fields


def safe_filename(name):
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", name.strip()).strip("_")
    return cleaned[:70] or "participant"


def make_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size=size) if font_path else ImageFont.load_default()
    except OSError:
        return ImageFont.load_default()


def render_certificates(template_file, rows, options, font_path=None):
    template_file.seek(0)
    base = Image.open(template_file).convert("RGB")
    name_font = make_font(font_path, options["font_size"])
    extra_specs = parse_extra_fields(options["extra_fields"])
    output = io.BytesIO()

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        used_names = {}
        for index, row in enumerate(rows, start=1):
            image = base.copy()
            draw = ImageDraw.Draw(image)

            name = row.get("name", "").strip()
            draw.text(
                (options["name_x"], options["name_y"]),
                name,
                fill=options["text_color"],
                font=name_font,
                anchor="mm",
            )

            for column, x, y, size, color in extra_specs:
                value = row.get(column, "")
                if value:
                    draw.text((x, y), value, fill=color,
                              font=make_font(font_path, size), anchor="mm")

            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG", optimize=True)

            stem = safe_filename(name)
            used_names[stem] = used_names.get(stem, 0) + 1
            suffix = f"_{used_names[stem]}" if used_names[stem] > 1 else ""
            archive.writestr(f"{index:03d}_{stem}{suffix}.png", image_bytes.getvalue())

    output.seek(0)
    return output, len(rows)
