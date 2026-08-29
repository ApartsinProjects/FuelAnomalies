#!/usr/bin/env bash
# Regenerate PDF + DOCX from index.html. Run from repo root.
set -e
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
# PDF (renders SVG + CSS; @media print hides the download box)
"$EDGE" --headless --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
  --virtual-time-budget=12000 --print-to-pdf="$PWD/FuelAnomalies.pdf" "file:///$PWD/index.html"
# DOCX (swap SVG->PNG for Word, strip download box, then pandoc)
python -c "import re;h=open('index.html',encoding='utf-8').read();h=re.sub(r'<div class=\"downloads\">.*?</div>\s*','',h,flags=re.S,count=1);h=h.replace('.svg\" alt','.png\" alt');open('_paper_docx.html','w',encoding='utf-8').write(h)"
pandoc _paper_docx.html -o FuelAnomalies.docx --resource-path=.
rm -f _paper_docx.html
echo "built FuelAnomalies.pdf and FuelAnomalies.docx"
