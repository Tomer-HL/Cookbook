import re
from pathlib import Path

# -----------------------------
# Parsing helpers
# -----------------------------
def extract_block(text, start_headers, stop_headers):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start_set = set(start_headers)
    stop_set = set(stop_headers)
    collecting = False
    collected = []

    for line in lines:
        stripped = line.strip()
        if stripped in start_set:
            collecting = True
            continue
        if collecting and stripped in stop_set:
            break
        if collecting:
            collected.append(line)
    return "\n".join(collected).strip()


def parse_list(block):
    lines = []
    for line in block.splitlines():
        clean = line.strip("•\t- ").strip()
        if clean:
            lines.append(clean)
    return lines


def parse_steps(block):
    text = block.replace("\r\n", "\n").replace("\r", "\n")
    raw_steps = re.split(r"\n\s*\n", text)
    steps = [s.strip() for s in raw_steps if s.strip()]
    return steps

# -----------------------------
# HTML builder
# -----------------------------
def build_html(title, ingredients, instructions, description,
               lang="en", time_text="40 minutes", level_text="Easy",
               hero_image=None, file_other="#"):
    is_he = lang == "he"
    direction = "rtl" if is_he else "ltr"
    font_family = "Alef, system-ui, sans-serif" if is_he else "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

    hero_tag = f'<img class="hero" src="{hero_image}" alt="{title}">' if hero_image else ""

    label_recipe = "מתכון" if is_he else "RECIPE"
    label_time = "זמן" if is_he else "Time"
    label_servings = "מנות" if is_he else "Servings"
    label_level = "רמת קושי" if is_he else "Level"
    label_ingredients = "מצרכים" if is_he else "Ingredients"
    label_instructions = "הוראות הכנה" if is_he else "Instructions"
    subtitle = "מנה קלאסית שקל להכין בבית." if is_he else "A classic dish you can easily make at home."
    lang_switch_text = (
        f'<img src="flag_gb.png" alt="English"> English' if is_he else f'<img src="flag_il.png" alt="עברית"> עברית'
    )

    html = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="UTF-8">
<title>{title}</title>

<style>
:root {{
    --main-orange: #d35400;
    --ingredient-bullet: #d35400;
    --section-bg: #fffaf0;
}}

body {{
    font-family: {font_family};
    background: linear-gradient(180deg, #fdf8f0 0%, #fffefc 100%);
    margin: 0;
    padding: 40px;
    display: flex;
    justify-content: center;
}}
.page {{
    max-width: 900px;
    width: 100%;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    padding: 28px 32px 32px;
    position: relative;
}}
.hero {{
    width: 100%;
    height: 260px;
    object-fit: cover;
    border-radius: 14px;
    margin-top: 20px;
    margin-bottom: 24px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}}
.lang-switch {{
    position: absolute;
    top: 16px;
    right: 16px;
    font-size: 14px;
    z-index: 15;
    display: flex;
    align-items: center;
    gap: 4px;
    text-decoration: none;
}}
.lang-switch img {{
    width: 20px;
    height: 14px;
}}
.header-bar {{
    height: 3px;
    background: var(--main-orange);
    border-radius: 2px;
    margin-bottom: 18px;
}}
.header {{
    margin-bottom: 20px;
}}
.tag {{
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
    color: #7a7a7a;
}}
h1 {{
    margin: 6px 0;
    font-size: 32px;
    color: var(--main-orange);
}}
.subtitle {{
    font-size: 15px;
    color: #666;
    margin-bottom: 10px;
}}
.description {{
    font-size: 15px;
    color: #444;
}}
.meta {{
    display: flex;
    gap: 24px;
    margin-top: 16px;
}}
.meta-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    color: #23412f;
}}
.meta-item span.icon {{
    font-size: 30px;
}}
.content {{
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    gap: 32px;
    margin-top: 28px;
}}
h2 {{
    font-size: 20px;
    margin-bottom: 10px;
    color: var(--main-orange);
}}
.section-box {{
    background: var(--section-bg);
    border: 1px solid #f7d8c5;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 16px;
}}
ul {{
    list-style: none;
    padding-{ 'right' if is_he else 'left' }: 28px;
    margin: 0;
}}
ul li {{
    position: relative;
    padding-{ 'right' if is_he else 'left' }: 28px;
    margin-bottom: 6px;
}}
ul li::before {{
    content: "❖";  /* מעוין כתום */
    color: var(--ingredient-bullet);
    position: absolute;
    { 'right' if is_he else 'left' }: 0;
}}
ol {{
    list-style: none;
    counter-reset: step-counter;
    padding-{ 'right' if is_he else 'left' }: 0;
    margin: 0;
}}
ol li {{
    counter-increment: step-counter;
    position: relative;
    margin-bottom: 14px;
    padding-{ 'right' if is_he else 'left' }: 36px;  /* יותר מקום למספר */
    font-size: 15px;
}}
ol li::before {{
    content: counter(step-counter);
    position: absolute;
    top: 0;
    { 'right' if is_he else 'left' }: 0;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--main-orange);
    color: #fff;
    text-align: center;
    line-height: 28px;
    font-weight: bold;
}}
.divider {{
    border-top: none;
    border-left: none;
    border-right: none;
    height: 2px;
    background: linear-gradient(to right, var(--main-orange) 10%, #fff 50%, var(--main-orange) 90%);
    margin: 20px 0;
}}
.print-button {{
    position: absolute;
    top: 16px;
    left: 16px;
    padding: 4px 8px;
    font-size: 12px
    border: none;
    border-radius: 5px;
    background: var(--main-orange);
    color: white;
    cursor: pointer;
    z-index: 20;
}}
.print-button:hover {{
    background: #e67e22;
}}
</style>
</head>

<body>
<div class="page">

<button class="print-button" onclick="window.print()">🖨️ {'הדפסה' if is_he else 'Print'}</button>

<div class="lang-switch">
    <a href="{file_other}">{lang_switch_text}</a>
</div>

{hero_tag}

<div class="header-bar"></div>

<div class="header">
    <div class="tag">{label_recipe}</div>
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
    <div class="description">{description}</div>

    <div class="meta">
        <div class="meta-item"><span class="icon">🕒</span> <b>{label_time}:</b> {time_text}</div>
        <div class="meta-item"><span class="icon">🍽️</span> <b>{label_servings}:</b> 4</div>
        <div class="meta-item"><span class="icon">🧑‍🍳</span> <b>{label_level}:</b> {level_text}</div>
    </div>
</div>

<div class="section-box">
    <h2>{label_ingredients}</h2>
    <ul>
        {''.join(f'<li>{i}</li>' for i in ingredients)}
    </ul>
</div>

<div class="divider"></div>

<div class="section-box">
    <h2>{label_instructions}</h2>
    <ol>
        {''.join(f'<li>{s}</li>' for s in instructions)}
    </ol>
</div>

</div>
</body>
</html>
"""
    return html

# -----------------------------
# Print version
# -----------------------------
def build_print(title, ingredients, instructions, description, lang="en"):
    is_he = lang == "he"
    direction = "rtl" if is_he else "ltr"
    label_ingredients = "מצרכים" if is_he else "Ingredients"
    label_instructions = "הוראות הכנה" if is_he else "Instructions"

    html = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="UTF-8">
<title>{title} – Print</title>
<style>
:root {{
    --main-orange: #d35400;
    --ingredient-bullet: #d35400;
    --section-bg: #fffaf0;
}}
body {{
    font-family: Georgia, serif;
    padding: 40px;
    max-width: 800px;
    margin: auto;
    line-height: 1.5;
    background: #fff;
}}
h1 {{
    font-size: 32px;
    margin-bottom: 10px;
    color: var(--main-orange);
}}
h2 {{
    margin-top: 28px;
    border-bottom: 2px solid var(--main-orange);
    padding-bottom: 4px;
    color: var(--main-orange);
}}
.section-box {{
    background: var(--section-bg);
    border: 1px solid #f7d8c5;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 16px;
}}
ul {{
    list-style: none;
    padding-{ 'right' if is_he else 'left' }: 28px;
    margin: 0;
}}
ul li {{
    position: relative;
    padding-{ 'right' if is_he else 'left' }: 28px;
    margin-bottom: 6px;
}}
ul li::before {{
    content: "●";
    color: var(--ingredient-bullet);
    position: absolute;
    { 'right' if is_he else 'left' }: 0;
}}
ol {{
    list-style: none;
    counter-reset: step-counter;
    padding-{ 'right' if is_he else 'left' }: 0;
    margin: 0;
}}
ol li {{
    counter-increment: step-counter;
    position: relative;
    margin-bottom: 14px;
    padding: 0 16px;
    font-size: 15px;
}}
ol li::before {{
    content: counter(step-counter);
    position: absolute;
    top: 0;
    { 'right' if is_he else 'left' }: 0;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--main-orange);
    color: #fff;
    text-align: center;
    line-height: 28px;
    font-weight: bold;
}}
.divider {{
    border-top: 1px dashed var(--main-orange);
    margin: 20px 0;
}}
.print-button {{
    display: inline-block;
    margin-bottom: 20px;
    padding: 8px 12px;
    font-size: 14px;
    border: none;
    border-radius: 6px;
    background: var(--main-orange);
    color: white;
    cursor: pointer;
}}
.print-button:hover {{
    background: #e67e22;
}}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="description">{description}</p>

<button class="print-button" onclick="window.print()">🖨️ {'הדפסה' if is_he else 'Print'}</button>

<div class="section-box">
    <h2>{label_ingredients}</h2>
    <ul>
        {''.join(f'<li>{i}</li>' for i in ingredients)}
    </ul>
</div>

<div class="divider"></div>

<div class="section-box">
    <h2>{label_instructions}</h2>
    <ol>
        {''.join(f'<li>{s}</li>' for s in instructions)}
    </ol>
</div>

</body>
</html>
"""
    return html

# -----------------------------
# Recipe parsing
# -----------------------------
def parse_recipe_file(path):
    text = Path(path).read_text(encoding="utf-8")
    title = text.splitlines()[0].strip()

    ingredients_block = extract_block(
        text,
        ["Ingredients", "מצרכים"],
        ["Instructions", "אופן ההכנה", "Description", "תיאור"]
    )

    instructions_block = extract_block(
        text,
        ["Instructions", "אופן ההכנה"],
        ["Ingredients", "מצרכים", "Description", "תיאור"]
    )

    description_block = extract_block(
        text,
        ["Description", "תיאור"],
        ["Ingredients", "מצרכים", "Instructions", "אופן ההכנה"]
    )

    ingredients = parse_list(ingredients_block)
    instructions = parse_steps(instructions_block)
    description = description_block.strip()

    return title, ingredients, instructions, description

# -----------------------------
# Main - הגדר כאן את פרטי המתכון
# -----------------------------
recipe_name = "Shakshuka"
txt_en = f"{recipe_name}_en.txt"
txt_he = f"{recipe_name}_he.txt"

# מחפש תמונה אוטומטית (.png/.jpg/.jpeg)
image_file = None
for ext in [".png", ".jpg", ".jpeg"]:
    possible_file = f"{recipe_name}{ext}"
    if Path(possible_file).exists():
        image_file = possible_file
        break
if image_file is None:
    print(f"⚠️ לא נמצאה תמונה עבור {recipe_name}. המתכון ייווצר בלי תמונה.")

# זמן ורמת קושי
time_en, level_en = "40 minutes", "Easy"
time_he, level_he = "40 דקות", "קל"

# קבצי HTML
file_en = f"{recipe_name}_en.html"
file_he = f"{recipe_name}_he.html"

# -----------------------------
# English
t, ing, inst, desc = parse_recipe_file(txt_en)
Path(file_en).write_text(
    build_html(t, ing, inst, desc, lang="en", time_text=time_en, level_text=level_en,
               hero_image=image_file, file_other=file_he),
    encoding="utf-8"
)
Path(f"{recipe_name}_en_print.html").write_text(
    build_print(t, ing, inst, desc, lang="en"),
    encoding="utf-8"
)

# Hebrew
t, ing, inst, desc = parse_recipe_file(txt_he)
Path(file_he).write_text(
    build_html(t, ing, inst, desc, lang="he", time_text=time_he, level_text=level_he,
               hero_image=image_file, file_other=file_en),
    encoding="utf-8"
)
Path(f"{recipe_name}_he_print.html").write_text(
    build_print(t, ing, inst, desc, lang="he"),
    encoding="utf-8"
)

print("✅ HTML + Print HTML created for EN + HE")