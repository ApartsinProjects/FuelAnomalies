#!/usr/bin/env bash
# Build the elsarticle (EAAI) LaTeX from index.html and compile. Run from repo root.
set -e
python scripts/make_latex.py
cd latex
for i in 1 2 3; do lualatex -interaction=nonstopmode -file-line-error FuelAnomalies.tex >/dev/null 2>&1 || true; done
echo "built latex/FuelAnomalies.pdf"
