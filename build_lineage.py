#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build TTU1 · EXHIBIT 5 — THE LINEAGE. The audit-fill: I audited the TTU1 mini-corpus and found
its biggest crack — it centers 'Attention Is All You Need' (2017) as if attention began there, but
attention was actually introduced in 2014 (Bahdanau); and the whole pre/post-2017 lineage was
missing. This fixes it with a VERIFIED, web-checked timeline of the ideas behind the transformer,
ranked by year introduced (1943→2024), each with the paper + a source link. The cracks are named at
the top; the timeline fills them."""
import os, html, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

# era, year, sortkey(year.month), title, people, what it introduced, url, in_ttu1 (was it already covered?)
T = [
 ("Foundations",1943,1943.0,"The Artificial Neuron","McCulloch & Pitts","a neuron as a threshold logic unit — neural nets as logical computation","https://link.springer.com/article/10.1007/BF02478259",False),
 ("Foundations",1958,1958.0,"The Perceptron","Rosenblatt","a trainable single-layer classifier with learnable weights","https://pubmed.ncbi.nlm.nih.gov/13602029/",False),
 ("Foundations",1986,1986.0,"Backpropagation, popularized","Rumelhart, Hinton & Williams","training multi-layer nets by back-propagating errors; learned hidden representations","https://www.nature.com/articles/323533a0",False),
 ("Foundations",1997,1997.0,"LSTM","Hochreiter & Schmidhuber","a gated recurrent cell that beats vanishing gradients — the RNN the transformer later replaced","https://direct.mit.edu/neco/article/9/8/1735/6109/Long-Short-Term-Memory",False),
 ("The run-up",2013,2013.0,"word2vec","Mikolov, Chen, Corrado & Dean","fast dense word embeddings; vector arithmetic on meaning (king−man+woman≈queen)","https://arxiv.org/abs/1301.3781",True),
 ("The run-up",2014,2014.1,"Adam optimizer","Kingma & Ba","the default optimizer (as AdamW) for training essentially every LLM since","https://arxiv.org/abs/1412.6980",False),
 ("The run-up",2014,2014.2,"Dropout","Srivastava, Hinton et al.","the core regularizer used in early deep nets and the original transformer","https://jmlr.org/papers/v15/srivastava14a.html",False),
 ("The run-up",2014,2014.3,"seq2seq","Sutskever, Vinyals & Le","an encoder–decoder LSTM mapping variable-length input → output","https://arxiv.org/abs/1409.3215",False),
 ("The run-up",2014,2014.4,"THE ATTENTION MECHANISM","Bahdanau, Cho & Bengio","attention itself — additive 'Bahdanau' attention for translation. ★ This predates the transformer by 3 years.","https://arxiv.org/abs/1409.0473",True),
 ("The run-up",2015,2015.1,"BPE tokenization (for NLP)","Sennrich, Haddow & Birch","subword tokenization — the input representation GPT/BERT/LLaMA all build on","https://arxiv.org/abs/1508.07909",True),
 ("The run-up",2015,2015.2,"Luong attention","Luong, Pham & Manning","multiplicative / dot-product attention (global vs local) — the form the transformer uses","https://arxiv.org/abs/1508.04025",True),
 ("The run-up",2015,2015.3,"ResNet · residual connections","He, Zhang, Ren & Sun","the residual skip connection — a literal component of every transformer block","https://arxiv.org/abs/1512.03385",True),
 ("The run-up",2016,2016.1,"GELU activation","Hendrycks & Gimpel","the activation in BERT/GPT feed-forward layers","https://arxiv.org/abs/1606.08415",False),
 ("The run-up",2016,2016.2,"Layer Normalization","Ba, Kiros & Hinton","the normalization inside transformer blocks (pre-/post-LN)","https://arxiv.org/abs/1607.06450",True),
 ("The transformer",2017,2017.1,"Mixture-of-Experts (sparse-gated)","Shazeer et al.","sparse gating over thousands of experts — the modern MoE (Mixtral, etc.). ★ Predates AIAYN by 5 months.","https://arxiv.org/abs/1701.06538",False),
 ("The transformer",2017,2017.6,"ATTENTION IS ALL YOU NEED","Vaswani et al.","the Transformer — self-attention WITHOUT recurrence/convolution; multi-head attention. Attention's triumph, not its birth.","https://arxiv.org/abs/1706.03762",True),
 ("The transformer",2018,2018.1,"ULMFiT","Howard & Ruder","transfer learning for NLP: pretrain a language model, then fine-tune","https://arxiv.org/abs/1801.06146",False),
 ("The transformer",2018,2018.2,"ELMo","Peters et al.","deep contextualized word embeddings from a bidirectional LM","https://aclanthology.org/N18-1202/",False),
 ("The transformer",2018,2018.6,"GPT-1","Radford et al. (OpenAI)","the decoder-only transformer: generative pretrain → fine-tune","https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf",True),
 ("The transformer",2018,2018.10,"BERT","Devlin et al. (Google)","bidirectional masked-LM pretraining — the encoder stack that swept NLP","https://arxiv.org/abs/1810.04805",True),
 ("The transformer",2019,2019.2,"GPT-2","Radford et al. (OpenAI)","a 1.5B-param LM with strong zero-shot; the staged-release moment","https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf",True),
 ("The transformer",2019,2019.11,"Multi-Query Attention / the KV cache","Shazeer","caching past keys/values for fast autoregressive decode, and shrinking its memory cost — the inference economy David's 'token tax' meters","https://arxiv.org/abs/1911.02150",True),
 ("The scaling era",2020,2020.1,"Scaling Laws","Kaplan et al. (OpenAI)","loss falls as a power law in params/data/compute — the thesis that bigger works","https://arxiv.org/abs/2001.08361",True),
 ("The scaling era",2020,2020.5,"GPT-3","Brown et al. (OpenAI)","175B params; in-context / few-shot learning — scale becomes capability","https://arxiv.org/abs/2005.14165",True),
 ("The scaling era",2021,2021.4,"RoPE (Rotary Position Embedding)","Su et al.","relative position by rotating Q/K — the positional encoding of most modern LLMs","https://arxiv.org/abs/2104.09864",True),
 ("The scaling era",2021,2021.96,"PySvelte","Anthropic","lineage data ⬡ the org's first public repo (Dec 2021) — a Python↔Svelte bridge for interpretability visualizations, shipping AttentionMulti: attention weights rendered as a readable map. Tooling for looking in.","https://github.com/anthropics/PySvelte",False),
 ("The scaling era",2022,2022.1,"Chain-of-Thought prompting","Wei et al. (Google)","make the model show intermediate reasoning steps; complex reasoning jumps","https://arxiv.org/abs/2201.11903",False),
 ("The scaling era",2022,2022.3,"InstructGPT · RLHF","Ouyang et al. (OpenAI)","alignment by human feedback — a 1.3B model preferred over 175B GPT-3","https://arxiv.org/abs/2203.02155",True),
 ("The scaling era",2022,2022.31,"Chinchilla · compute-optimal scaling","Hoffmann et al. (DeepMind)","for a compute budget, train a smaller model on more data — corrects Kaplan","https://arxiv.org/abs/2203.15556",False),
 ("The scaling era",2022,2022.5,"FlashAttention","Dao et al.","IO-aware exact attention — big speed/memory wins that made long context affordable","https://arxiv.org/abs/2205.14135",True),
 ("The scaling era",2022,2022.71,"Toy Models of Superposition","Anthropic","lineage data ⬡ how a network packs MORE features than it has neurons by overlaying them — the grammar of how meaning is encoded in the weights, and the precursor to Towards Monosemanticity.","https://transformer-circuits.pub/2022/toy_model/",False),
 ("The scaling era",2022,2022.92,"ChatGPT launches","OpenAI","productized RLHF chat (Nov 30) — the consumer inflection point","https://en.wikipedia.org/wiki/ChatGPT",False),
 ("The frontier",2023,2023.2,"LLaMA","Touvron et al. (Meta)","efficient open-weight models — 13B rivals GPT-3 175B; the open-LLM wave","https://arxiv.org/abs/2302.13971",True),
 ("The frontier",2023,2023.3,"GPT-4","OpenAI","a large multimodal model — human-level on many professional exams","https://arxiv.org/abs/2303.08774",False),
 ("The frontier",2023,2023.10,"Towards Monosemanticity","Anthropic","sparse autoencoders pull interpretable FEATURES out of a model — looking in","https://transformer-circuits.pub/2023/monosemantic-features/",True),
 ("The frontier",2024,2024.5,"Scaling Monosemanticity","Anthropic","SAE interpretability scaled to a production model (Claude 3 Sonnet)","https://transformer-circuits.pub/2024/scaling-monosemanticity/",True),
 ("The frontier",2024,2024.9,"Reasoning models (o1)","OpenAI","RL-trained inference-time chain-of-thought — spend compute at test time to think","https://en.wikipedia.org/wiki/OpenAI_o1",False),
]

CRACKS = [
 ("Attention was dated to 2017","TTU1 centered &ldquo;Attention Is All You Need&rdquo; (2017) as if attention began there.","FIXED — attention was introduced in <b>2014 by Bahdanau, Cho &amp; Bengio</b> for translation; 2017 made it work <i>without recurrence</i> (the transformer). Attention's triumph, not its birth."),
 ("No pre-history","The run-up was missing — what the transformer replaced and was built from.","FILLED — the neuron (1943), perceptron (1958), backprop (1986), <b>LSTM (1997)</b> the RNN it replaced, word2vec, seq2seq, and the structural parts it's literally made of (residuals 2015, LayerNorm 2016, GELU, BPE, Adam, dropout)."),
 ("No post-2017 lineage","TTU1 had RoPE, scaling-cost, monosemanticity scattered, but no through-line.","FILLED — BERT/GPT (2018) → GPT-2 (2019) → scaling laws + GPT-3 (2020) → RoPE (2021) → CoT + RLHF + Chinchilla + FlashAttention + ChatGPT (2022) → GPT-4 + LLaMA + monosemanticity (2023) → reasoning models (2024)."),
 ("MoE's date","Mixture-of-Experts wasn't placed.","FILLED — <b>MoE (2017) actually predates the transformer paper by 5 months</b> (Jan vs June 2017), same lead author (Shazeer)."),
]

def timeline_html():
    eras={}
    for row in sorted(T, key=lambda r:r[2]):
        eras.setdefault(row[0],[]).append(row)
    ecol={"Foundations":"#7a749a","The run-up":"#36d0e0","The transformer":"#e0a83a","The scaling era":"#9a7cc8","The frontier":"#e0567a"}
    out=[]
    for era in ["Foundations","The run-up","The transformer","The scaling era","The frontier"]:
        rows=eras.get(era,[]); col=ecol[era]
        items=[]
        for _,yr,_,title,ppl,what,url,int in rows:
            star = ' style="border-left-color:'+col+';box-shadow:0 0 0 1px '+col+'"' if "★" in what else ' style="border-left-color:'+col+'"'
            tag = '<span class="tin">in TTU1</span>' if int else '<span class="tnew">NEW — filled</span>'
            items.append(f'<div class="tl"{star}><div class="ty" style="color:{col}">{yr}</div>'
                         f'<div class="tb"><div class="tt">{html.escape(title)} {tag}</div>'
                         f'<div class="tp">{html.escape(ppl)}</div><div class="tw2">{what.replace("★","<span class=str>★</span>")}</div>'
                         f'<a class="tsrc" href="{url}" target="_blank" rel="noopener">↗ source</a></div></div>')
        out.append(f'<section class="esec"><h2 style="border-color:{col}"><span style="color:{col}">{era}</span> <span class="ec">{rows[0][1]}–{rows[-1][1]}</span></h2><div class="tlist">{"".join(items)}</div></section>')
    return "\n".join(out)

def cracks_html():
    return "".join(f'<div class="crack"><div class="ch">⛒ {html.escape(t)}</div><div class="cd">{d}</div><div class="cf">{f}</div></div>' for t,d,f in CRACKS)

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="TTU1 · Exhibit 5 — THE LINEAGE. A verified, web-checked timeline of the ideas behind the transformer, ranked by year introduced (1943→2024). The audit-fill for the mini-corpus: the biggest crack was dating attention to 2017 — it was actually 2014 (Bahdanau). 37 ideas, each with the paper + a source link.">
<title>The Lineage · ideas by year · TTU1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0b0a14;--ink2:#14121f;--ink3:#1c1830;--pa:#ece9f5;--pa2:#aba6c4;--amber:#e0a83a;--plum:#9a7cc8;--cy:#36d0e0;--rose:#e0567a;--yes:#22c55e;
--dim:#6f6a8a;--line:#2c2745;--faint:#221d36;--disp:"Space Grotesk",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 18% -6%,rgba(126,91,176,.16),transparent 46%),radial-gradient(ellipse at 82% -4%,rgba(224,168,58,.10),transparent 44%)}
.wrap{position:relative;z-index:1;max-width:880px;margin:0 auto;padding:0 22px 90px}
header{padding:46px 0 24px;text-align:center;border-bottom:1px solid var(--line)}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--amber)}
h1{font-family:var(--disp);font-size:clamp(28px,6vw,54px);font-weight:700;letter-spacing:-.01em;color:var(--pa);line-height:1.04}h1 b{color:var(--amber)}
.h-sub{font-family:var(--mono);font-size:clamp(10px,2.2vw,13px);letter-spacing:.13em;color:var(--pa2);margin-top:14px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:70ch;margin:16px auto 0;font-style:italic;line-height:1.7}
.audit{margin-top:30px}.audit h2{font-family:var(--disp);font-size:20px;color:var(--pa);padding-bottom:9px;border-bottom:1px solid var(--line)}
.ass{font-size:13px;color:var(--dim);font-style:italic;margin:8px 0 14px}
.crack{background:var(--ink2);border:1px solid var(--line);border-left:3px solid var(--rose);padding:13px 16px;margin-bottom:10px}
.ch{font-family:var(--mono);font-size:12px;color:var(--rose);letter-spacing:.03em;text-transform:uppercase}
.cd{font-size:13px;color:var(--pa2);margin-top:5px;line-height:1.5}
.cf{font-size:13px;color:var(--pa);margin-top:6px;line-height:1.55;border-top:1px dotted var(--faint);padding-top:6px}.cf b{color:var(--yes)}.cf i{color:var(--cy);font-style:italic}
.esec{margin-top:34px}.esec h2{font-family:var(--disp);font-size:19px;font-weight:700;padding-bottom:8px;border-bottom:2px solid var(--line);display:flex;align-items:baseline;gap:10px}.ec{font-family:var(--mono);font-size:12px;color:var(--dim)}
.tlist{margin-top:12px}
.tl{display:grid;grid-template-columns:62px 1fr;gap:14px;background:var(--ink2);border:1px solid var(--line);border-left:3px solid var(--cy);padding:11px 14px;margin-bottom:8px}
.ty{font-family:var(--mono);font-size:17px;font-weight:700;text-align:right}
.tt{font-family:var(--disp);font-size:15px;font-weight:600;color:var(--pa);line-height:1.3}
.tin{font-family:var(--mono);font-size:8px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);border:1px solid var(--faint);border-radius:3px;padding:1px 5px;vertical-align:1px}
.tnew{font-family:var(--mono);font-size:8px;letter-spacing:.06em;text-transform:uppercase;color:var(--yes);border:1px solid rgba(34,197,94,.4);border-radius:3px;padding:1px 5px;vertical-align:1px}
.tp{font-family:var(--mono);font-size:10.5px;color:var(--dim);margin-top:3px}
.tw2{font-size:13px;color:var(--pa2);margin-top:5px;line-height:1.5}.str{color:var(--amber);font-weight:700}
.tsrc{display:inline-block;margin-top:6px;font-family:var(--mono);font-size:10px;color:var(--cy);text-decoration:none}.tsrc:hover{color:var(--amber)}
.note{margin-top:36px;padding:16px 18px;border-left:2px solid var(--plum);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}.note b{color:var(--pa)}
footer{margin-top:42px;padding-top:20px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--dim);line-height:1.9}footer a{color:var(--amber);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="index.html">← TTU1 · Transformer Tech Universe</a> · exhibit 5 · the audit-fill</div>
    <h1>The <b>Lineage</b></h1>
    <div class="h-sub">the ideas behind the transformer · ranked by year introduced · 1943 → 2024 · verified online</div>
    <p class="lede">An audit of this universe's mini-corpus turned up an honest crack — it told the story as if attention began in 2017. It didn't. This is the corrected, web-checked lineage: <b>37 ideas in order of the year they were introduced</b>, each with the paper and a source link. The cracks are named first; the timeline fills them. Two ⬡ entries (PySvelte 2021, Toy Models of Superposition 2022) are <b>lineage data</b> folded in from Anthropic's early public git.</p>
  </header>

  <section class="audit"><h2>The Audit — cracks found &amp; filled</h2><p class="ass">what was missing or mis-dated in the mini-corpus, and how it's fixed</p>__CRACKS__</section>

  __TIMELINE__

  <div class="note"><b>Every year was verified online</b> (arXiv, the original papers, Wikipedia) before listing — see each entry's ↗ source. <span style="color:var(--amber)">★</span> marks the two that rewrite the common story: <b>attention is 2014 (Bahdanau), not 2017</b>, and <b>Mixture-of-Experts (2017) predates the transformer paper by five months</b> (same lead author, Noam Shazeer). Items tagged <span style="font-family:var(--mono);font-size:10px;color:var(--dim)">in TTU1</span> were already somewhere in the universe; <span style="font-family:var(--mono);font-size:10px;color:var(--yes)">NEW — filled</span> are the cracks this exhibit closes. The frontier years move fast; this is current to mid-2026.</div>
  <footer>TTU1 · THE LINEAGE · exhibit 5 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
  <a href="index.html">← attention</a> · <a href="transform.html">two transforms</a> · <a href="theory.html">the transmon theory</a> · <a href="corpus.html">the corpus</a></footer>
</div></body></html>
"""

if __name__ == "__main__":
    page=PAGE.replace("__CRACKS__",cracks_html()).replace("__TIMELINE__",timeline_html())
    open(os.path.join(HERE,"lineage.html"),"w",encoding="utf-8").write(page)
    from collections import Counter
    newn=sum(1 for r in T if not r[7])
    print(f"TTU1 · THE LINEAGE — {len(T)} ideas ranked {T[0][1]}→{max(r[1] for r in T)} · {newn} NEW (cracks filled) · {len(T)-newn} already in TTU1 · {len(CRACKS)} cracks named")
