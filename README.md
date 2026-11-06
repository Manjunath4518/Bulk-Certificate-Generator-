# Bulk Certificate Generator

A Django + Pillow application for generating personalized certificates in batches.

## Features
- Upload a certificate background/template (PNG or JPG).
- Upload participant details as a CSV file.
- Configure the name position, font size, and text color.
- Generate one PNG certificate per participant.
- Download all generated certificates in a ZIP file.
- Keeps the original template unchanged.

## 1. Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## 2. Prepare the CSV

The CSV must contain a `name` column. Other columns are optional and can be inserted into the certificate using placeholders.

Example:

```csv
name,course,date,organization
Aarav Sharma,Python Workshop,06 November 2026,Vardhaman College
Diya Reddy,AI Bootcamp,06 November 2026,Vardhaman College
```

## 3. Prepare the template

Use a PNG or JPG certificate design. Upload it from the home page.

Coordinates are measured in pixels from the top-left corner of the uploaded image. Configure:
- X position: horizontal center point for the name
- Y position: vertical position for the name
- Font size: size in pixels
- Text color: hex color such as `#202020`

The name is centered horizontally at X. Text is drawn with a TrueType font when available; Pillow's default font is used otherwise.

## 4. Placeholders

You can add additional text fields using the optional `Extra fields` box. Use one field per line in this format:

```text
course|900|760|36|#222222
date|900|900|24|#444444
organization|900|980|24|#444444
```

Format: `column_name|x|y|font_size|#hexcolor`

The `name` field is configured separately. Each field is centered at its X coordinate.

## Notes
- The uploaded CSV is validated before generation.
- Each output filename is made safe for download.
- Generation is synchronous and suitable for small/medium event batches. For very large batches, move generation to a background worker.
- Uploaded files are stored under `media/`. Do not expose this development configuration directly to the public internet without adding authentication, upload limits, and production storage settings.
