#!/bin/bash

# -----------------------------
# Config - שנה לפי הצורך
# -----------------------------
REPO_DIR="$HOME/.local/share/Cookbook"   # נתיב למיקום הפרויקט שלך ב‑WSL
PYTHON_SCRIPT="generate_recipe.py"         # השם של הסקריפט שלך
COMMIT_MSG="Update recipes HTML + images"

# -----------------------------
# Run Python script
# -----------------------------
echo "🚀 Running Python script..."
python3 "$REPO_DIR/$PYTHON_SCRIPT"

# -----------------------------
# Git add & commit & push
# -----------------------------
cd "$REPO_DIR" || exit
echo "📦 Adding changes to git..."
git add .

echo "✏️ Committing changes..."
git commit -m "$COMMIT_MSG"

echo "📤 Pushing to GitHub..."
git push origin main   # אם הסניף שלך שונה מ-main, שנה בהתאם

echo "✅ Done! All updates pushed to GitHub."
