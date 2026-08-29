#!/usr/bin/env bash
# Regenerate DOCX (pandoc, native equations) then PDF (LibreOffice from the DOCX). Run from repo root.
set -e
SOFFICE="/c/Program Files/LibreOffice/program/soffice.exe"
W="$(pwd -W 2>/dev/null)"; WINROOT="${W//\//\\}"
# DOCX: svg->png for Word; strip download box; parse \(..\)/\[..\] math to native OMML equations
python -c "import re;h=open('index.html',encoding='utf-8').read();h=re.sub(r'<div class=\"downloads\">.*?</div>\s*','',h,flags=re.S,count=1);h=h.replace('.svg\" alt','.png\" alt');open('_paper_docx.html','w',encoding='utf-8').write(h)"
pandoc -f html+tex_math_single_backslash _paper_docx.html -o FuelAnomalies.docx --resource-path=.
rm -f _paper_docx.html
# PDF: LibreOffice DOCX->PDF (native equations + figures). Windows-style profile path is REQUIRED
# (a /tmp-style path makes soffice hang). Kill any running instance first.
taskkill //F //IM soffice.exe //IM soffice.bin >/dev/null 2>&1 || true
"$SOFFICE" --headless --norestore --convert-to pdf --outdir "$WINROOT" "$WINROOT\FuelAnomalies.docx" \
  "-env:UserInstallation=file:///C:/Users/apart/lo_fa_profile" 2>&1 | tail -1
echo "built FuelAnomalies.docx and FuelAnomalies.pdf"
