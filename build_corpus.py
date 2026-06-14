#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build TTU1 · EXHIBIT 3 — THE CORPUS. David asked: check the Downloads folder for transmon-fit,
and "if not, add everything in the corpus into one file of the transmon or transformer tech."
The Downloads corpus is overwhelmingly computing / Series-E / inference material, so it docks here,
under TRANSFORMER TECH. This consolidates the ENTIRE Downloads body of work (every .html + .zip)
into ONE indexed file, each item honestly tagged by which universe it belongs to. The genuinely-new
transformer-tech instruments — the 52-Card ISA (the Deck → a base-52 instruction set), the Toroid
Inference Engine (a recurrent ternary loop), and the Veracity Ledger (a doped-toroid inference
engine + 2026 industry state) — are copied in and linked LIVE. Honest: most of the rest is already
cataloged in MIMZY (Series-E) or PROPULSION-LAB (energy), and is marked so, not re-claimed."""
import os, html, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DL = r"C:\Users\Dave\Downloads"
CORPUS_DIR = os.path.join(HERE, "corpus")
os.makedirs(CORPUS_DIR, exist_ok=True)

# the three genuinely-new transformer-tech instruments → copied in, served live
FEATURED = {
 "card-instruction-set.html":   ("The 52-Card Instruction Set", "the Deck → a base-52 ISA: suit = operation family, rank = the operation. Program in playing cards — the sequel to TTU1's Deck."),
 "toroid-inference-engine.html":("The Toroid Inference Engine", "a recurrent ternary loop where the 0 is BOTH the activation and the abstain — inference as a loop through the zero."),
 "veracity-ledger.html":        ("The Veracity Ledger", "a doped-toroid inference engine measured against the real 2026 industry: 596 neuromorphic-compute patents, +401% in 2025 — provenance turned on itself."),
}
for fn in FEATURED:
    src = os.path.join(DL, fn)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(CORPUS_DIR, fn))

def title_of(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read(4000)
        m = re.search(r"<title>([^<]*)</title>", t, re.I)
        return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else ""
    except Exception:
        return ""

# classification by filename keyword → (bucket, home)
def classify(fn):
    n = fn.lower()
    if any(k in n for k in ["card-instruction","toroid-inference","veracity-ledger","render-step","two-probe","sideways","two-depths","tropical-router","attention","transformer-inference"]):
        return "ttu1"
    if any(k in n for k in ["qubit","quantum_dot","quantum-dot","phosphor","arsenic","silicon","nucleus","the-gap-live","island-run","entangled","transmon","new-processor","processor-design"]):
        return "transmon"
    if any(k in n for k in ["kernel-27","chronos","cipher","coding-theory","compiler-lineage","delta-protocol","dual-descent","ignition","lattice-of-lattices","nested-shells","planetary-core","rotating-core","ternary-hamming","torus-ride","twelve-gate","two-axis-gap","three-blueprints","two-walkers","three-in-a-circle","duty-cycle","extraction-cycle"]):
        return "seriesE"
    if any(k in n for k in ["wireless-energy","wormhole","anti-gravity","einstein-lens","gravity_tensor","gravity-","ball_lightning","aeonic","octet-holonomy","oscillation-engine","pulsar_fractal","toroid-builder","wave_modulator"]):
        return "energy"
    if "karsa" in n:
        return "karsa"
    return "other"

BUCKETS = {
 "ttu1":    ("#e0a83a","TRANSFORMER TECH (this universe)","inference, the ISA, the render step, the quadrature read — computing the transformer way"),
 "transmon":("#8b5cf6","TRANSMON · quantum hardware","the quantum-hardware artifacts — silicon, dopant qubits, the band gap, entanglement, the nucleus (home: the transmon universe)"),
 "seriesE": ("#22d3ee","SERIES-E · already in MIMZY","the kernel/witness/ternary/torus instruments — built &amp; audited in the MIMZY forge; listed here for completeness"),
 "energy":  ("#5fd06a","ENERGY · PROPULSION-LAB","wireless power, the wormhole, gravitational lensing, ball lightning — David's energy/propulsion toolkits (home: PROPULSION LAB)"),
 "karsa":   ("#e0567a","KARSA · the variants","the many karsa-* render/skin variants — one engine, many costumes"),
 "other":   ("#9a7cc8","GOVERNANCE · IP · MISC","law, provenance, OS, site, kernel, and assorted artifacts — the rest of the body of work"),
}
ORDER = ["ttu1","transmon","seriesE","energy","karsa","other"]

def human(fn):
    base = re.sub(r"\.(html|htm|zip)$","",fn,flags=re.I)
    return base.replace("-"," ").replace("_"," ")

def build_items():
    files = sorted(os.listdir(DL))
    items = []  # (bucket, fn, kind, title, featured)
    for fn in files:
        low = fn.lower()
        if low.endswith((".html",".htm")):
            kind="page"
        elif low.endswith(".zip"):
            kind="zip"
        else:
            continue
        if fn == "ud0.html":  # the biosphere index snapshot — skip
            continue
        b = classify(fn)
        t = title_of(os.path.join(DL,fn)) if kind=="page" else ""
        items.append((b, fn, kind, t, fn in FEATURED))
    return items

def section_html(items):
    out=[]
    for b in ORDER:
        col,name,desc = BUCKETS[b]
        mem=[it for it in items if it[0]==b]
        if not mem: continue
        rows=[]
        for _,fn,kind,t,feat in sorted(mem, key=lambda x:(0 if x[4] else 1, x[1].lower())):
            label = html.escape(t) if t else html.escape(human(fn))
            sub = html.escape(human(fn)) if t else ("toolkit (.zip)" if kind=="zip" else "")
            kindtag = "▸ LIVE" if feat else ("page" if kind=="page" else "zip")
            link = (f'corpus/{fn}' if feat else "")
            name_el = (f'<a class="ci-n" href="{link}">{label}</a>' if feat else f'<span class="ci-n">{label}</span>')
            rows.append(f'<div class="ci{ " feat" if feat else ""}"><div class="ci-k" style="color:{col if feat else "var(--dim)"}">{kindtag}</div>'
                        f'<div class="ci-b">{name_el}<span class="ci-s">{sub}</span></div></div>')
        out.append(f'<section class="csec" id="{b}"><h2 style="border-color:{col}"><span style="color:{col}">{name}</span> <span class="cct">{len(mem)}</span></h2>'
                   f'<p class="css">{desc}</p><div class="cgrid">{"".join(rows)}</div></section>')
    return "\n".join(out), len(items)

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="TTU1 · Exhibit 3 — THE CORPUS. The entire Downloads body of work consolidated into one file, every item tagged by home universe: transformer-tech, transmon (quantum hardware), Series-E (MIMZY), energy (PROPULSION-LAB), karsa, and misc. The three genuine new transformer-tech instruments — the 52-Card ISA, the Toroid Inference Engine, the Veracity Ledger — are live.">
<title>The Corpus · TTU1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0b0a14;--ink2:#14121f;--ink3:#1c1830;--pa:#ece9f5;--pa2:#aba6c4;--amber:#e0a83a;--plum:#9a7cc8;--cy:#36d0e0;--rose:#e0567a;
--dim:#6f6a8a;--faint:#221d36;--line:#2c2745;--disp:"Space Grotesk",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.62;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 18% -6%,rgba(126,91,176,.16),transparent 46%),radial-gradient(ellipse at 82% -4%,rgba(224,168,58,.10),transparent 44%)}
.wrap{position:relative;z-index:1;max-width:960px;margin:0 auto;padding:0 22px 90px}
header{padding:44px 0 22px;text-align:center;border-bottom:1px solid var(--line)}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--amber)}
h1{font-family:var(--disp);font-size:clamp(28px,6vw,54px);font-weight:700;letter-spacing:-.01em;color:var(--pa);line-height:1.04}h1 b{color:var(--amber)}
.h-sub{font-family:var(--mono);font-size:clamp(10px,2.2vw,13px);letter-spacing:.14em;color:var(--pa2);margin-top:14px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:70ch;margin:16px auto 0;font-style:italic;line-height:1.72}
.tot{font-family:var(--mono);font-size:12px;color:var(--amber);margin-top:14px;letter-spacing:.06em}
.csec{margin-top:40px}.csec h2{font-family:var(--disp);font-size:20px;font-weight:600;color:var(--pa);padding-bottom:9px;border-bottom:2px solid var(--line);display:flex;align-items:baseline;gap:10px}
.cct{font-family:var(--mono);font-size:12px;color:var(--dim)}
.css{font-size:13px;color:var(--dim);font-style:italic;margin:8px 0 14px;line-height:1.55}
.cgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}@media(max-width:680px){.cgrid{grid-template-columns:1fr}}
.ci{display:flex;gap:10px;align-items:baseline;background:var(--ink2);border:1px solid var(--line);padding:9px 12px}
.ci.feat{border-color:var(--amber);background:rgba(224,168,58,.06)}
.ci-k{font-family:var(--mono);font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;flex:0 0 42px;white-space:nowrap}
.ci-b{min-width:0}.ci-n{font-size:13.5px;color:var(--pa);text-decoration:none;display:block;line-height:1.3}a.ci-n:hover{color:var(--amber)}
.ci-s{font-family:var(--mono);font-size:9.5px;color:var(--dim);display:block;margin-top:2px;overflow:hidden;text-overflow:ellipsis}
.feat-note{margin-top:8px;font-size:12.5px;color:var(--pa2);font-style:italic;line-height:1.5}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--plum);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}.note b{color:var(--pa)}
footer{margin-top:42px;padding-top:20px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--dim);line-height:1.9}footer a{color:var(--amber);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="index.html">← TTU1 · Transformer Tech Universe</a> · exhibit 3</div>
    <h1>The <b>Corpus</b></h1>
    <div class="h-sub">the whole Downloads body of work · one file · honestly tagged</div>
    <p class="lede">You asked: does the Downloads folder fit the transmon universe — and if not, put the whole corpus into one file under the transmon or transformer tech. It's <b>mostly transformer-tech / computing / Series-E</b>, so it docks here. This is every loose artifact in <span style="font-family:var(--mono);color:var(--pa)">C:\\Users\\Dave\\Downloads</span> — consolidated, grouped, and tagged by which universe it actually belongs to. Three genuinely-new transformer-tech instruments are <b style="color:var(--amber)">live</b>; the rest is honestly attributed (most is already built in MIMZY or PROPULSION-LAB).</p>
    <div class="tot">__TOTAL__ artifacts indexed · 3 new instruments live</div>
  </header>

  <div class="note" style="border-left-color:var(--amber);margin-top:24px"><b>The three new ones, built in &amp; live (▸):</b> <b>The 52-Card Instruction Set</b> — your Deck (TTU1 Exhibit 1) turned into a base-52 ISA, suit = op-family, rank = operation; the natural sequel to the card encoding. <b>The Toroid Inference Engine</b> — a recurrent ternary loop where the 0 is both the activation and the abstain. <b>The Veracity Ledger</b> — a doped-toroid inference engine measured against the real 2026 neuromorphic-compute industry (596 patents, +401% in 2025). Click any ▸ LIVE item to run it.</div>

  __SECTIONS__

  <div class="note"><b>Honest tagging, not re-claiming.</b> This file CONSOLIDATES the corpus into one index; it does not re-mint things that already have a home. The <span style="color:var(--cy)">Series-E</span> items are already live in the <a href="https://davidwise01.github.io/mimzy/" style="color:var(--cy)">MIMZY</a> forge; the <span style="color:#5fd06a">energy</span> toolkits belong to <a href="https://davidwise01.github.io/propulsion-lab/" style="color:#5fd06a">PROPULSION LAB</a>; the <span style="color:var(--plum)">quantum-hardware</span> ones to the <a href="https://davidwise01.github.io/transmon/" style="color:var(--plum)">transmon universe</a>. Only the three transformer-tech instruments are newly built in here. The corpus is a snapshot of the Downloads folder at build time.</div>
  <footer>TTU1 · THE CORPUS · exhibit 3 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
  <a href="index.html">← the attention exhibit</a> · <a href="transform.html">the two transforms</a> · <a href="https://davidwise01.github.io/ud0/">the biosphere →</a></footer>
</div></body></html>
"""

if __name__ == "__main__":
    items = build_items()
    secs, total = section_html(items)
    page = PAGE.replace("__SECTIONS__", secs).replace("__TOTAL__", str(total))
    open(os.path.join(HERE, "corpus.html"), "w", encoding="utf-8").write(page)
    from collections import Counter
    c = Counter(it[0] for it in items)
    print(f"TTU1 · THE CORPUS — {total} artifacts indexed · buckets {dict(c)} · {len([f for f in FEATURED if os.path.exists(os.path.join(CORPUS_DIR,f))])} live instruments copied")
