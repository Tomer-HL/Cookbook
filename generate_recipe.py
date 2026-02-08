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

    # תקן את הנתיב של התמונה
    hero_tag = f'<img class="hero" src="images/{hero_image}" alt="{title}">' if hero_image else ""

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
/* ... כל שאר ה-CSS נשאר זהה ... */
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
# Print version נשאר זהה
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
/* ... כל ה-CSS של הדפסה ... */
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
# Main
# -----------------------------
recipe_name = "Shakshuka"
txt_en = f"{recipe_name}_en.txt"
txt_he = f"{recipe_name}_he.txt"

# מחפש תמונה בתיקיית images/
image_file = None
for ext in [".png", ".jpg", ".jpeg"]:
    possible_file = f"images/{recipe_name}{ext}"
    if Path(possible_file).exists():
        image_file = f"{recipe_name}{ext}"  # HTML יוסיף "images/"
        break
if image_file is None:
    print(f"⚠️ לא נמצאה תמונה עבור {recipe_name}. המתכון ייווצר בלי תמונה.")

# זמן ורמת קושי
time_en, level_en = "40 minutes", "Easy"
time_he, level_he = "40 דקות", "קל"

# קבצי HTML
file_en = f"{recipe_name}_en.html"
file_he = f"{recipe_name}_he.html"

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

print("✅ HTML + Print HTML created for EN + HE, images/ path fixed!")