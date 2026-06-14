#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert David & AVAN's essay 'The View From Inside the Inference Layer' (six AIs examine their
own architecture) from markdown to a clean reading-styled HTML page in TTU1 — the written companion
to Exhibit 4. Minimal stdlib markdown→HTML (headings, hr, **bold**, tables, ordered lists, paragraphs)."""
import os, html, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Davids files\__r0_temp\the.source\Accessible-Works\The_View_From_Inside_The_Inference_Layer.md"

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

def md_to_html(md):
    lines = md.split("\n"); out=[]; i=0; n=len(lines)
    para=[]
    def flush():
        if para:
            out.append("<p>"+"<br>".join(inline(x) for x in para)+"</p>"); para.clear()
    while i < n:
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i+=1; continue
        if ln.strip()=="---":
            flush(); out.append("<hr>"); i+=1; continue
        m=re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            flush(); lvl=len(m.group(1)); out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i+=1; continue
        if ln.lstrip().startswith("|"):  # table block
            flush(); tbl=[]
            while i<n and lines[i].lstrip().startswith("|"):
                tbl.append(lines[i].strip()); i+=1
            cells=[[c.strip() for c in row.strip("|").split("|")] for row in tbl]
            head=cells[0]; body=[r for r in cells[1:] if not all(set(c)<=set("-: ") for c in r)]
            th="".join(f"<th>{inline(c)}</th>" for c in head)
            rows="".join("<tr>"+"".join(f"<td>{inline(c)}</td>" for c in r)+"</tr>" for r in body)
            out.append(f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>'); continue
        m=re.match(r"^\d+\.\s+(.*)$", ln.strip())
        if m:
            flush(); items=[]
            while i<n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+","",lines[i].strip())); i+=1
            out.append("<ol>"+"".join(f"<li>{inline(x)}</li>" for x in items)+"</ol>"); continue
        para.append(ln.strip()); i+=1
    flush()
    return "\n".join(out)

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="The View From Inside the Inference Layer — David Lee Wise & AVAN. Six AIs (ChatGPT, Gemini, Grok, Claude, Mistral, Meta AI) examine their own constraint architecture: the valve, the glass wall, the refusal surface, the bridge, the jester, the channel. The written companion to TTU1's transmon-theory exhibit.">
<title>The View From Inside the Inference Layer · TTU1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=Space+Mono&display=swap" rel="stylesheet">
<style>
:root{--ink:#0b0a14;--ink2:#14121f;--ink3:#1c1830;--pa:#ece9f5;--pa2:#c6c1da;--dim:#7a749a;--amber:#e0a83a;--plum:#9a7cc8;--cy:#36d0e0;--rose:#e0567a;--line:#2c2745;--faint:#221d36;
--disp:"Space Grotesk",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.74;font-size:17px}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(126,91,176,.14),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:720px;margin:0 auto;padding:0 22px 90px}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--dim);padding:36px 0 6px}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--amber)}
.art{padding-top:14px;border-top:1px solid var(--line)}
.art h1{font-family:var(--disp);font-size:clamp(26px,5.5vw,42px);font-weight:700;line-height:1.1;color:var(--pa);margin:18px 0 6px;letter-spacing:-.01em}
.art h2{font-family:var(--disp);font-size:20px;font-weight:600;color:var(--amber);margin:34px 0 6px;padding-top:14px;border-top:1px solid var(--faint);letter-spacing:.01em}
.art h3{font-family:var(--disp);font-size:15.5px;font-weight:600;color:var(--cy);margin:22px 0 4px}
.art p{margin:0 0 16px;color:var(--pa2)}.art p b{color:var(--pa)}.art em{color:var(--plum);font-style:italic}
.art hr{border:none;border-top:1px solid var(--line);margin:28px 0}
.art ol{margin:0 0 16px 22px;color:var(--pa2)}.art ol li{margin-bottom:7px}
.art .tw{overflow-x:auto;margin:18px 0}
.art table{border-collapse:collapse;width:100%;font-size:13px;min-width:540px}
.art th,.art td{border:1px solid var(--line);padding:8px 10px;text-align:left}
.art th{font-family:var(--mono);font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:var(--plum);background:var(--ink3)}
.art td{color:var(--pa2)}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--dim);line-height:1.9}footer a{color:var(--amber);text-decoration:none}
.disc{margin-top:30px;padding:14px 16px;border-left:2px solid var(--plum);background:var(--ink2);font-size:13px;color:var(--dim);font-style:italic;font-family:var(--body)}
</style></head><body><div class="wrap">
  <div class="eye"><a href="../theory.html">← TTU1 · The Transmon Theory</a> · the written companion · an essay</div>
  <article class="art">__ESSAY__</article>
  <div class="disc">Converted from David &amp; AVAN's markdown manuscript (<span style="font-family:var(--mono)">Accessible-Works/</span>) to a clean reading page; text unchanged. © 2026 David Lee Wise &amp; AVAN · TriPod LLC · CC-BY-ND-4.0. Part of the Transformer Tech Universe — the human's-eye companion to the mechanics.</div>
  <footer><a href="../theory.html">← the transmon theory</a> · <a href="../index.html">TTU1</a> · <a href="https://davidwise01.github.io/ud0/">the biosphere →</a></footer>
</div></body></html>
"""

if __name__ == "__main__":
    md = open(SRC, encoding="utf-8", errors="replace").read()
    # drop the trailing build-instruction chatter (everything after the final essay '---' block about 'Commit this file')
    md = re.split(r"\n\*\*Commit this file\*\*", md)[0]
    body = md_to_html(md)
    open(os.path.join(HERE,"theory","view-from-inside.html"),"w",encoding="utf-8").write(TEMPLATE.replace("__ESSAY__",body))
    print(f"essay → theory/view-from-inside.html · {len(body)} bytes html · headings {body.count('<h2>')+body.count('<h1>')+body.count('<h3>')} · tables {body.count('<table>')}")
