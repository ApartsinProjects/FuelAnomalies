"""Build an elsarticle (EAAI single-column) LaTeX source from index.html.
Outputs latex/FuelAnomalies.tex (+ latex/body.tex). Figures referenced from ../figures (PNG).
Run pandoc + pdflatex separately (see build_latex.sh)."""
import os, re, html, subprocess
ROOT=os.path.join(os.path.dirname(__file__),".."); LT=os.path.join(ROOT,"latex"); os.makedirs(LT,exist_ok=True)
h=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()

# --- abstract (strip tags, keep math + entities) ---
ab=re.search(r'<p class="lead">(.*?)</p>',h,re.S).group(1)
ab=re.sub(r'<[^>]+>',' ',ab); ab=html.unescape(ab); ab=re.sub(r'\s+',' ',ab).strip()

# --- body: Introduction through end of References list ---
start=h.index('<h2 id="intro">'); end=h.index('</ol>',h.index('id="r25"'))+5
body=h[start:end]
body=body.replace('figures/','')           # graphicspath handles dir
body=body.replace('.svg" alt','.png" alt') # LaTeX needs raster
# drop the fixed download box if present, and the algorithm's raw entities are fine
frag=os.path.join(LT,"_frag.html"); open(frag,"w",encoding="utf-8").write("<body>"+body+"</body>")

subprocess.run(["pandoc","-f","html+tex_math_single_backslash","-t","latex",frag,
                "-o",os.path.join(LT,"body.tex")],check=True)
bt=open(os.path.join(LT,"body.tex"),encoding="utf-8").read()
# fix display math with \tag{n} -> numbered equation environment
bt=re.sub(r'\\\[(.*?)\\tag\{(\d+)\}\s*\\\]', lambda m:'\\begin{equation}'+m.group(1)+'\\end{equation}', bt, flags=re.S)
# includegraphics: cap width
bt=bt.replace('\\includegraphics{','\\includegraphics[width=\\linewidth]{')
# pandoc emits \tightlist sometimes
bt=bt.replace('\\tightlist','')
open(os.path.join(LT,"body.tex"),"w",encoding="utf-8").write(bt)

main=r'''\documentclass[preprint,11pt]{elsarticle}
\usepackage{amsmath,amssymb,graphicx,booktabs,array,longtable,calc,url,hyperref}
\graphicspath{{../figures/}}
\journal{Engineering Applications of Artificial Intelligence}
\begin{document}
\begin{frontmatter}
\title{Driver or Vehicle? Multi-Source Signature Attribution of Excess Fuel Consumption Under Missing Joint Cause Labels}
\author[hit]{Alexander Apartsin}
\author[afeka]{Yehudit Aperstein}
\affiliation[hit]{organization={School of Computer Science, Faculty of Sciences, Holon Institute of Technology (HIT)},city={Holon},country={Israel}}
\affiliation[afeka]{organization={Intelligent Systems, Afeka Academic College of Engineering},city={Tel-Aviv},country={Israel}}
\begin{abstract}
%ABSTRACT%
\end{abstract}
\begin{keyword}
fuel consumption \sep anomaly attribution \sep driver behaviour \sep engine fault diagnosis \sep multi-source learning \sep explainable AI
\end{keyword}
\end{frontmatter}
\input{body.tex}
\end{document}
'''.replace('%ABSTRACT%',ab)
open(os.path.join(LT,"FuelAnomalies.tex"),"w",encoding="utf-8").write(main)
os.remove(frag)
print("wrote latex/FuelAnomalies.tex and latex/body.tex; abstract chars:",len(ab))
