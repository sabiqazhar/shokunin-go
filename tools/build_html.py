#!/usr/bin/env python3
"""Gabungkan README + docs/*.md menjadi satu halaman HTML (termasuk render Mermaid) untuk dibaca offline dan dibagikan.

Cara pakai:
    python3 tools/build_html.py            # menghasilkan handbook.html
    python3 tools/build_html.py -o x.html
"""
from __future__ import annotations

import argparse
import html as _html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Butuh python-markdown: pip3 install markdown")

ROOT = Path(__file__).resolve().parent.parent

# (file, judul bab). Urutan = urutan daftar isi
FILES = [
    ("README.md", "Ringkasan dan Cara Tim Menjalankannya"),
    ("docs/01-phase1-go-internals.md", "Fase 1 · Internals Go dan Memori"),
    ("docs/02-phase2-concurrency-os.md", "Fase 2 · Konkurensi dan Sistem Operasi"),
    ("docs/03-phase3-networking.md", "Fase 3 · Jaringan dan Protokol"),
    ("docs/04-phase4-storage-engine.md", "Fase 4 · Storage Engine"),
    ("docs/05-phase5-distributed-systems.md", "Fase 5 · Sistem Terdistribusi"),
    ("docs/06-phase6-production-design.md", "Fase 6 · Desain Production-Grade"),
    ("docs/07-weekly-schedule-24w.md", "Jadwal Mingguan 24 Pekan"),
    ("docs/08-code-review-and-quality-gates.md", "Standar Code Review dan Quality Gate"),
    ("docs/09-tooling-cheatsheet.md", "Cheatsheet Tooling"),
    ("docs/10-templates.md", "Kumpulan Template Dokumen"),
]

MD_EXT = ["extra", "tables", "fenced_code", "toc", "attr_list", "sane_lists"]
MD_EXT_CFG = {"toc": {"slugify": lambda v, s: re.sub(r"[^\w\u4e00-\u9fff-]", "-", v).lower()}}

MERMAID_RE = re.compile(
    r'<pre><code\s+class="[^"]*mermaid[^"]*">(.*?)</code></pre>',
    re.DOTALL,
)

CSS = """
:root{
  --bg:#ffffff; --fg:#1f2328; --muted:#57606a; --line:#d8dee4;
  --accent:#0969da; --accent-soft:#ddf4ff; --code-bg:#f6f8fa;
  --warn-bg:#fff8c5; --warn-line:#d4a72c; --ok-bg:#dafbe1; --ok-line:#1a7f37;
  --bad-bg:#ffebe9; --bad-line:#cf222e;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
#layout{display:flex; align-items:flex-start; max-width:1500px; margin:0 auto}
#sidebar{
  position:sticky; top:0; height:100vh; overflow-y:auto;
  width:300px; flex:0 0 300px; padding:24px 16px 60px;
  border-right:1px solid var(--line); background:#fbfcfd; font-size:14px;
}
#sidebar h1{font-size:17px; margin:0 0 4px}
#sidebar .sub{color:var(--muted); font-size:12px; margin-bottom:18px}
#sidebar ol{list-style:none; padding-left:0; margin:0}
#sidebar li{margin:2px 0}
#sidebar a{
  display:block; padding:6px 10px; border-radius:6px;
  color:var(--fg); text-decoration:none; line-height:1.45;
}
#sidebar a:hover{background:var(--accent-soft); color:var(--accent)}
#sidebar a.active{background:var(--accent); color:#fff}
#content{flex:1 1 auto; min-width:0; padding:32px 40px 120px}
h1.doc-title{font-size:30px; margin:0 0 8px; padding-bottom:12px; border-bottom:2px solid var(--line)}
h2{font-size:24px; margin:44px 0 14px; padding-bottom:8px; border-bottom:1px solid var(--line)}
h3{font-size:19px; margin:30px 0 10px}
h4{font-size:16px; margin:22px 0 8px; color:var(--muted)}
p{margin:12px 0}
a{color:var(--accent)}
ul,ol{padding-left:26px}
li{margin:5px 0}
blockquote{
  margin:16px 0; padding:12px 16px; border-left:4px solid var(--accent);
  background:var(--accent-soft); color:#0b3161; border-radius:0 6px 6px 0;
}
blockquote p{margin:6px 0}
code{
  font-family:"SFMono-Regular",Menlo,Consolas,"Liberation Mono",monospace;
  font-size:.88em; background:var(--code-bg); padding:2px 6px; border-radius:4px;
}
pre{
  background:var(--code-bg); border:1px solid var(--line); border-radius:8px;
  padding:14px 16px; overflow:auto; line-height:1.55;
}
pre code{background:none; padding:0; font-size:13px}
table{border-collapse:collapse; width:100%; margin:16px 0; font-size:14.5px; display:block; overflow-x:auto}
th,td{border:1px solid var(--line); padding:8px 12px; text-align:left; vertical-align:top}
th{background:#f0f3f6; font-weight:600}
tr:nth-child(even) td{background:#fafbfc}
hr{border:0; border-top:1px solid var(--line); margin:36px 0}
.mermaid{
  margin:20px 0; padding:14px; background:#fbfcfd;
  border:1px solid var(--line); border-radius:8px; overflow-x:auto; text-align:center;
}
.mermaid pre{background:none;border:0;text-align:left}
.section-nav{
  display:flex; justify-content:space-between; gap:12px;
  margin:56px 0 24px; padding-top:18px; border-top:1px solid var(--line); font-size:14px;
}
.badge{display:inline-block; padding:1px 8px; border-radius:10px; font-size:12px; font-weight:600}
.b-ok{background:var(--ok-bg); color:var(--ok-line)}
.b-warn{background:var(--warn-bg); color:#7a5b00}
.b-bad{background:var(--bad-bg); color:var(--bad-line)}
h2 .anchor{float:left; margin-left:-22px; opacity:.28; font-weight:400; text-decoration:none}
h2:hover .anchor{opacity:.8}
#toggle{
  position:fixed; left:8px; bottom:12px; z-index:50; display:none;
  background:var(--accent); color:#fff; border:0; border-radius:20px;
  padding:8px 14px; font-size:13px; cursor:pointer;
}
@media (max-width:1000px){
  #sidebar{position:fixed; transform:translateX(-100%); transition:.2s; z-index:40; background:#fff; box-shadow:0 0 20px rgba(0,0,0,.15)}
  #sidebar.open{transform:none}
  #content{padding:20px 18px 100px}
  #toggle{display:block}
}
"""

JS = """
// Mermaid
window.mermaidConfigReady = false;
function bootMermaid(){
  if (window.mermaid && !window.mermaidConfigReady) {
    window.mermaidConfigReady = true;
    mermaid.initialize({
      startOnLoad: false, securityLevel: 'loose', theme: 'default',
      flowchart: { curve: 'basis', useMaxWidth: true, htmlLabels: true },
      sequence: { useMaxWidth: true, wrap: true },
      themeVariables: { fontSize: '14px', fontFamily: 'system-ui, -apple-system, Segoe UI, sans-serif' }
    });
    mermaid.run({ querySelector: '.mermaid' });
  }
}

// Sorot daftar isi
(function(){
  var links = Array.prototype.slice.call(document.querySelectorAll('#sidebar a[href^="#"]'));
  var sections = links.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); });
  function onScroll(){
    var y = window.scrollY + 90, idx = 0;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i] && sections[i].offsetTop <= y) idx = i;
    }
    links.forEach(function(a, i){ a.classList.toggle('active', i === idx); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// Tombol buka/tutup sidebar (layar sempit)
(function(){
  var b = document.getElementById('toggle'), s = document.getElementById('sidebar');
  if (b && s) b.addEventListener('click', function(){ s.classList.toggle('open'); });
})();
"""


def md_to_html(text: str) -> str:
    conv = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_EXT_CFG)
    return conv.convert(text)


def convert_mermaid(html: str) -> str:
    def repl(m: re.Match) -> str:
        body = _html.unescape(m.group(1))
        return f'<div class="mermaid">{_html.escape(body)}</div>'

    return MERMAID_RE.sub(repl, html)


def slugify(title: str, idx: int) -> str:
    return f"sec-{idx}"


def build(out: Path) -> None:
    parts_head: list[str] = []
    nav: list[str] = []
    body: list[str] = []

    for idx, (rel, title) in enumerate(FILES):
        path = ROOT / rel
        if not path.exists():
            print(f"[warn] tidak ditemukan {rel}", file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8")
        # buang H1 milik file, pakai judul bab yang seragam
        raw = re.sub(r"^#\s+.*?\n", "", raw, count=1).lstrip("\n")
        anchor = slugify(title, idx)
        nav.append(f'<li><a href="#{anchor}">{_html.escape(title)}</a></li>')
        body.append(f'<section id="{anchor}">')
        body.append(f'<h1 class="doc-title">{_html.escape(title)}</h1>')
        body.append(convert_mermaid(md_to_html(raw)))
        body.append("</section>")
        parts_head.append(rel)

    # beri anchor pada tiap h2 agar sidebar bisa menunjuk sub-bab
    doc = "\n".join(body)

    html_doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Panduan Engineering Go Tingkat Lanjut · 24 Pekan</title>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  window.mermaid = mermaid;
  bootMermaid();
</script>
<script>
  // Fallback saat CDN tidak tersedia: tetap tampilkan teks sumber
  window.addEventListener('load', function(){{
    setTimeout(function(){{
      if (!window.mermaid) {{
        document.querySelectorAll('.mermaid').forEach(function(d){{
          d.style.whiteSpace = 'pre-wrap'; d.style.fontFamily = 'monospace'; d.style.fontSize = '13px';
        }});
      }}
    }}, 3000);
  }});
</script>
<style>{CSS}</style>
</head>
<body>
<button id="toggle">Daftar isi</button>
<div id="layout">
  <nav id="sidebar">
    <h1>Panduan Go Tingkat Lanjut</h1>
    <div class="sub">24 pekan · low-level dan desain sistem</div>
    <ol>
{chr(10).join("      " + n for n in nav)}
    </ol>
  </nav>
  <main id="content">
{doc}
  </main>
</div>
<script>{JS}</script>
</body>
</html>
"""

    out.write_text(html_doc, encoding="utf-8")
    print(f"Selesai: {out}  ({len(doc)} karakter, {len(nav)} bab)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(ROOT / "handbook.html"))
    a = ap.parse_args()
    build(Path(a.out))

