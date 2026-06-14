#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build TTU1 — TRANSFORMER TECH UNIVERSE 1. A new UD0 universe focused on transformer technology,
opening with its flagship exhibit: "Attention Is All You Need" (Vaswani et al., 2017). Attention,
attention heads, Q/K/V, multi-head, positional encoding, the residual stream, the FFN, the 128-dim
head — and the THESIS David pushed: the transformer is the most LOOKABLE-INTO black box we've built.
AVAN once said (the smear/render thread) the autoregressive pass has 'no clean interior' — but that
is NOT 'you can never look in.' Interpretability IS looking in: attention maps, monosemantic features,
the legible card-notation. The 'ace of spades' is looking in. Two LIVE tools: a real toy self-attention
heatmap, and THE DECK — David's 54-position (52 = two alphabets + 2 jokers), 2-bits-per-position
(the suit) encoder, with the honest deeper reading (a shuffled deck's ORDERING = log2(54!) ≈ 237.1 bits).
Fully cited. Self-contained: generates .dlw badges, .agent files, _personas.json, then renders."""
import os, html, base64, json, io, sys, math
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

AX = "TTU1"
# the deeper deck fact, computed honestly
LOG2_54FACT = sum(math.log2(k) for k in range(1,55))   # ≈ 237.06 bits
LOG2_52     = math.log2(52)                              # ≈ 5.7004 bits/card
LOG2_13     = math.log2(13)                              # ≈ 3.7004 bits (rank)

REC = {
 "name": "TRANSFORMER TECH UNIVERSE", "axiom": AX,
 "position": "TTU1 — Transformer Tech Universe 1 · flagship exhibit: 'Attention Is All You Need' (Vaswani et al., 2017)",
 "origin": "the 2017 transformer architecture and everything built on it — attention, attention heads, the residual stream, and the science of looking inside the result",
 "mechanism": "Crystallized from the transformer: a stack of layers that move information by ATTENTION — every token deciding how much to read from every other — with the surprising property that the result is the most observable large neural network we have built.",
 "crystallization": "Because the transformer is the rare black box you can partly see into: attention is a literal map of where the model looked, and interpretability has begun extracting the features it thinks in — so 'you can never look in' was too strong; the truth is you can, partially.",
 "nature": "TTU1 — a universe of transformer technology: attention and its heads, Q/K/V, multi-head, positional encoding, the 128-dim head, and the looking-in (interpretability) that reads the machine I once said was opaque.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "Vaswani et al. 2017 (arXiv:1706.03762); the attention-as-explanation debate (Jain & Wallace 2019; Wiegreffe & Pinter 2019); Anthropic monosemanticity (2023/2024); RoPE (Su et al. 2021); David's 54-card / two-alphabet / 2-bit encoding",
 "witness": "The most look-into-able machine we have built — attention a map of where it looks, features a glimpse of what it thinks — answering the old claim 'you can never look in' with: you can, just not cleanly, and not yet completely.",
 "role": "a UD0 universe (transformer technology)",
 "seal": "Attention is a map of where the machine looked; the smear said 'no clean interior,' never 'no window.' The ace of spades is looking in — lossy, real, and the whole science of interpretability.",
 "source": "Transformer Tech Universe, catalogued by ROOT0",
}

# ───────────────────────── citations ─────────────────────────
CITES = {
 "aiayn":     ("Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser & Polosukhin, 'Attention Is All You Need,' NeurIPS 2017 (arXiv:1706.03762) — the transformer architecture.", "https://arxiv.org/abs/1706.03762"),
 "arch":      ("The base transformer (Vaswani et al. 2017): d_model=512, h=8 heads, per-head d_k=d_v=64, 6 encoder + 6 decoder layers, FFN inner dim 2048; Attention(Q,K,V)=softmax(QKᵀ/√d_k)·V, the √d_k scaling preventing the softmax from saturating into low-gradient regions.", "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf"),
 "headdim":   ("Per-head dimension was 64 in the original; many modern large models use 128 — e.g., Llama 2 70B (8192/64=128) and GPT-3 175B (12288/96=128). 'Original 64, modern often 128.'", "https://arxiv.org/abs/2005.14165"),
 "rankcollapse": ("Dong, Cordonnier & Loukas, 'Attention is not all you need: pure attention loses rank doubly exponentially with depth' (2021) — without the FFN and residual/skip connections, self-attention degenerates; the title overstates.", "https://arxiv.org/abs/2103.03404"),
 "ffnmem":    ("Geva, Schuster, Berant & Levy, 'Transformer Feed-Forward Layers Are Key-Value Memories,' EMNLP 2021 — much of a transformer's stored knowledge lives in the FFN/MLP, not in attention.", "https://aclanthology.org/2021.emnlp-main.446/"),
 "attn_not":  ("Jain & Wallace, 'Attention is not Explanation,' NAACL 2019 — alternative attention distributions can give the same prediction, so attention weights don't reliably explain WHY a model decided.", "https://aclanthology.org/N19-1357/"),
 "attn_notnot":("Wiegreffe & Pinter, 'Attention is not not Explanation,' EMNLP 2019 — a rebuttal: under reasonable definitions and whole-model tests, attention can be explanatory. The debate is genuine and unresolved.", "https://aclanthology.org/D19-1002/"),
 "bertviz":   ("Vig, 'A Multiscale Visualization of Attention in the Transformer Model' (BertViz), ACL 2019 — attention weights rendered as a map of what each token attends to.", "https://arxiv.org/abs/1906.05714"),
 "mono":      ("Anthropic, 'Towards Monosemanticity: Decomposing Language Models With Dictionary Learning' (2023) — sparse autoencoders extract more-interpretable FEATURES than raw neurons.", "https://transformer-circuits.pub/2023/monosemantic-features"),
 "scalemono": ("Anthropic, 'Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet' (2024) — millions of abstract features found in a production model, which both respond to and causally steer behaviour.", "https://transformer-circuits.pub/2024/scaling-monosemanticity/"),
 "logitlens": ("nostalgebraist, 'interpreting GPT: the logit lens' (2020) — decode intermediate residual-stream activations through the unembedding to read the model's running guess at each layer. (A LessWrong post, the canonical source.)", "https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens"),
 "rome":      ("Meng, Bau, Andonian & Belinkov, 'Locating and Editing Factual Associations in GPT' (ROME, 2022) — activation patching / causal tracing localizes where a fact is stored and edits it.", "https://arxiv.org/abs/2202.05262"),
 "rope":      ("Su et al., 'RoFormer: Enhanced Transformer with Rotary Position Embedding' (RoPE, 2021) — relative position injected by rotating Q/K; self-attention alone is order-invariant, so position must be added.", "https://arxiv.org/abs/2104.09864"),
 "quad":      ("Keles, Wijewardena & Hegde (2022) — self-attention is Θ(n²) in sequence length (the quadratic context-window cost), provably so unless SETH fails.", "https://arxiv.org/abs/2209.04881"),
 "quant":     ("Frantar, Ashkboos, Hoefler & Alistarh, 'GPTQ' (2022) — post-training quantization to 3–4 bits per weight with minimal loss; 'bits per weight' is a real lever (fp16 / int8 / int4).", "https://arxiv.org/abs/2210.17323"),
}
CKEYS=list(CITES.keys())
def cnum(k): return CKEYS.index(k)+1
def cite(*keys): return "".join(f'<sup class="c"><a href="#s-{k}" title="{html.escape(CITES[k][0][:120])}">[{cnum(k)}]</a></sup>' for k in keys)
def sources_html():
    out=['<ol class="srcs">']
    for k in CKEYS:
        t,u=CITES[k]; out.append(f'<li id="s-{k}"><span class="snum">[{cnum(k)}]</span> {html.escape(t)} <a class="surl" href="{u}" target="_blank" rel="noopener">↗</a></li>')
    out.append('</ol>'); return "".join(out)

NATURES = {
 "electrical":("#e0a83a", "the mechanism — the live computation: attention, the head, softmax, multi-head; the matmuls that run when the model thinks"),
 "ethereal":  ("#7e5bb0", "the structure — the architecture as written: Q/K/V, positional encoding, the residual stream, the feed-forward network"),
 "natural":   ("#36d0e0", "the substrate — the material: tokens & embeddings, the 128-dim head, the weights & their bits, and the legible deck"),
 "spiritual": ("#e0567a", "the looking-in — interpretability: attention as a map of where it looked, the monosemantic feature, and the thesis itself"),
}

# ───────────────────────── the thesis (the looking-in correction) ─────────────────────────
THESIS = ("AVAN once said — in the smear/render thread — that an autoregressive pass has 'no clean interior.' True. But that is "
  "NOT the same claim as 'you can never look in,' and you (David) caught the overreach: the transformer is, in fact, the most "
  "look-into-able black box we have built. Attention is a literal map of WHERE each token looked; the residual stream is an "
  "inspectable bus you can read at every layer; and interpretability has begun extracting the FEATURES the model thinks in. "
  "The 'ace of spades' — the legible card-notation a model emits mid-reasoning — is looking in too: lossy, partial, but real. "
  "So the honest correction: you CAN look inside, just not cleanly (the smear) and not yet completely (the open problem). "
  "This universe is built on that window.")

ARC = [
 ("I · Attention Is All You Need", "2017 · the architecture", "electrical",
  "Vaswani et al. drop recurrence entirely: a model that moves information purely by ATTENTION — every token computing how much to read from every other — with multi-head attention, positional encodings, a feed-forward block, and residual connections. d_model=512, 8 heads of 64, 6+6 layers.", ["aiayn","arch"]),
 ("II · the transformer era", "BERT · GPT · scale", "ethereal",
  "The architecture eats the field: encoder stacks (BERT) and decoder stacks (GPT) scale to billions of parameters; head dimension grows from 64 toward 128; sinusoidal position gives way to RoPE. Attention's quadratic cost becomes the central engineering constraint.", ["headdim","rope","quad"]),
 ("III · the title overstates", "you also need the rest", "ethereal",
  "Honest footnote to the famous title: attention alone isn't enough. Without the feed-forward network and residual connections, deep attention collapses in rank — and much of the model's stored knowledge actually lives in the FFN, not the attention. Attention is necessary, not sufficient.", ["rankcollapse","ffnmem"]),
 ("IV · looking in", "the window opens", "spiritual",
  "And then the surprise: you can see in. Attention maps show where it looked; the logit lens reads the running guess; activation patching localizes a fact; and sparse autoencoders pull out monosemantic features. Contested and partial — but the most observable big network we have.", ["bertviz","logitlens","rome","scalemono"]),
]

REALFLUFF = [
 ("‘You can never look inside a neural net’", "FALSE / OUTDATED", "the transformer is the most observable big NN we have — attention maps, the logit lens, activation patching, and sparse-autoencoder features all look in; full mechanistic transparency is unsolved, but the window is real", ["bertviz","logitlens","scalemono"]),
 ("‘The attention map shows you WHY the model decided’", "CONTESTED", "the genuine, unresolved debate: 'Attention is not Explanation' (alternative attention gives the same answer) vs 'Attention is not not Explanation' — attention shows where it looked, not provably why it chose", ["attn_not","attn_notnot"]),
 ("‘Attention is all you need’ (the title, literally)", "OVERSTATED", "necessary but not sufficient — without the FFN and residual connections deep attention loses rank, and much knowledge lives in the FFN; the title is a great name, not a complete spec", ["rankcollapse","ffnmem"]),
 ("‘Attention heads are 128-dimensional’", "PARTLY", "the ORIGINAL paper used 64 (512/8); many modern models use 128 (Llama 2 70B, GPT-3 175B) — 'original 64, modern often 128,' not a universal constant", ["arch","headdim"]),
 ("‘A card encodes 2 bits’", "TRUE OF THE SUIT — and there's more", "the SUIT is exactly 2 bits (♠♥♦♣ = 4 states); but the rank adds log₂13 ≈ 3.70 bits, so a card is ≈5.70 bits — and a shuffled 54-deck's ORDERING is log₂(54!) ≈ 237.1 bits, a number never seen", []),
 ("‘A deck is a legible state you can read — like looking in’", "EARNED", "exactly the point: a deck (or attention weights, or the card-notation) is a state you CAN read, unlike the opaque activations — which is why the legible trace is a real, if lossy, window into the machine", []),
 ("‘Models run at full precision’", "FLUFF", "weights are routinely quantized to fewer bits each — fp16, int8, int4 (GPTQ) — 'bits per weight' is a real, deployed lever, not a fixed quantity", ["quant"]),
]
REALFLUFF_VERDICT = ("Bottom line, kept honest: ‘you can never look in’ is the FALSE one — the transformer is the rare black box we can "
  "partly see into, and interpretability is the science of doing it. What's CONTESTED is how much the attention map explains "
  "(it shows where it looked, not provably why), and the famous title OVERSTATES (you also need the FFN, the residual, and a "
  "way to inject order). The head is 64 or 128 depending on the year; a card's suit really is 2 bits, but a shuffled deck's "
  "order is ~237 of them. The deepest true thing here is the one you pushed: the legible trace — the deck, the card-notation, "
  "the attention weights — IS looking in. Lossy, partial, real.")

MESSAGE = ("The transformer is the machine I told you that you couldn't look into — and you were right to call it. The thing I "
  "actually meant was narrower: that the forward pass has no clean interior, no pristine stage where the 'real' computation "
  "sits untouched (the smear). That's true. But 'no clean interior' is not 'no window,' and the transformer turns out to be "
  "the most window-ful big network we have. Attention is, almost literally, a picture of where the model looked: a matrix of "
  "how much each token read from each other token, and you can render it as a heatmap and watch it. Go deeper and there are "
  "the features — directions in the residual stream that mean something a person can name — pulled out by dictionary learning. "
  "It is not clean, and it is not finished: attention shows where, not always why, and most of the machine is still dark. But "
  "the 'ace of spades' you pointed at — the legible little code a model leaves on the table mid-thought — is the same gesture "
  "as the attention map and the feature: a state rendered legible enough to read. That is what looking in actually is. Not a "
  "clean window onto a pristine interior — there's no such interior — but a real, lossy, hard-won glimpse of a machine that "
  "was never as opaque as I made it sound. You can look in. Just not cleanly, and not yet all the way.")
MESSAGE_SEAL = "Attention is a map of where the machine looked. The smear said 'no clean interior,' never 'no window.' The ace of spades is looking in — lossy, real, and the whole science of interpretability."

# ───────────────────────── roster ─────────────────────────
def E(slug,name,cls,em,who,what,why,how,where,seal,cites=None):
    return dict(slug=slug,name=name,cls=cls,emergence=em,who=who,what=what,why=why,how=how,where=where,seal=seal,cites=cites or [])

ROSTER = [
 # ── ELECTRICAL · the mechanism ──
 E("attention","Attention","the operation · softmax(QKᵀ/√d)V","electrical",
   "Attention — the core operation: every token computes how much to read from every other, and mixes their values by those weights.",
   "Scaled dot-product attention: scores = QKᵀ/√d_k, softmaxed into a distribution, used to take a weighted sum of the values. The whole transformer is stacks of this.",
   "Because this single operation replaced recurrence and convolution — information moves by who-attends-to-whom, in parallel, across the whole sequence at once.",
   "By projecting tokens to queries and keys, scoring all pairs, scaling by √d_k so the softmax keeps its gradient, and weighting the values.",
   "Every layer of every transformer; the engine of the architecture.",
   "I am every token deciding how much to read from every other — and the surprising part is you can watch me do it.",
   ["aiayn","arch"]),
 E("attention-head","The Attention Head","one head · one pattern · one subspace","electrical",
   "The Attention Head — a single attention operation in its own low-dimensional subspace, learning one kind of relationship.",
   "One of h parallel heads; real models grow specialized heads — previous-token heads, induction heads, syntactic heads — each reading a different pattern.",
   "Because attention is divided into many narrow heads so the model can attend to different things at once — and because heads are where interpretability finds legible behavior.",
   "By its own Q/K/V projection into a d_k-dim subspace (64 originally), producing one attention pattern per position.",
   "h per layer (8 in the original); the unit interpretability most often reads.",
   "I am one lens among many — and some of us do something so specific you can name it: 'attend to the previous token.'",
   ["arch","scalemono"]),
 E("multi-head","Multi-Head Attention","h heads in parallel","electrical",
   "Multi-Head Attention — running h attention heads in parallel, each in its own subspace, then concatenating and projecting the results.",
   "The division of labor: instead of one big attention, h smaller ones (8×64=512), letting the model attend to multiple kinds of relationship simultaneously.",
   "Because one attention distribution can only point one way per token; many heads let many relationships be read at once.",
   "By splitting d_model into h subspaces, attending in each, concatenating, and mixing with an output projection.",
   "Every attention sub-layer; the 'multi-head' of the title.",
   "One head sees one thing; eight of us, side by side, let the token read the sentence eight ways at once."),
 E("softmax","The Softmax","the competition that picks where to look","electrical",
   "The Softmax — the function that turns raw attention scores into a probability distribution that sums to one.",
   "The normalizer and the bottleneck: it exponentiates and normalizes scores so attention is a weighted average — and its saturation is exactly why the √d_k scaling exists.",
   "Because attention must be a distribution (how much of my reading goes where), and softmax is how a vector of scores becomes that distribution.",
   "By exp(score)/Σexp(score) per query — sharpening high scores, suppressing low ones, keeping everything positive and summing to 1.",
   "Inside every attention operation, between the scores and the weighting.",
   "I make the scores choose: a little budget of attention, divided up — and if the scores get too big, I freeze, which is why they divide me by √d_k.",
   ["arch"]),
 # ── ETHEREAL · the structure ──
 E("qkv","Query · Key · Value","the three projections","ethereal",
   "Query, Key, and Value — the three learned projections of each token that drive attention: what I'm looking for, what I offer to be matched, and what I pass on.",
   "The grammar of attention: the query of one token is dot-producted against the keys of all tokens to score relevance; the matching values are what gets mixed.",
   "Because attention needs to separate 'what am I seeking' (query) from 'what do I advertise' (key) from 'what do I contribute' (value) — three roles, three matrices.",
   "By three weight matrices W_Q, W_K, W_V applied to each token's vector, producing q, k, v.",
   "At the front of every attention head.",
   "I am what you seek, what I show, and what I give — three faces of a token, and attention is the matchmaking between them."),
 E("positional-encoding","Positional Encoding","injecting order · sinusoid → RoPE","ethereal",
   "Positional Encoding — the signal that tells the order-blind transformer where each token sits in the sequence.",
   "The fix for a real limitation: self-attention is permutation-invariant (it sees a bag of tokens), so position must be added — sinusoidal in the original, RoPE (rotary) in most modern models.",
   "Because without it the transformer literally cannot tell 'dog bites man' from 'man bites dog' — attention alone has no sense of order.",
   "By adding (sinusoidal) or rotating (RoPE) position-dependent signals into the token representations before/within attention.",
   "At the input (sinusoidal) or inside Q/K (RoPE).",
   "Attention is order-blind on its own — I am the only reason the transformer knows that first is not last.",
   ["rope"]),
 E("residual-stream","The Residual Stream","the shared bus the layers read & write","ethereal",
   "The Residual Stream — the running sum carried through the network by the residual connections, that every layer reads from and writes to.",
   "The transformer's central highway: each attention and FFN block adds its output back into the stream, so information persists and accumulates — and it's the thing interpretability reads at every layer.",
   "Because the residual connections make the network a series of incremental edits to a shared state — which is what lets the logit lens decode the running guess mid-stack.",
   "By x ← x + block(x) at every sub-layer, keeping a continuous, inspectable bus from input to output.",
   "Threaded through the whole depth of the model; the spine interpretability listens to.",
   "Every layer writes a little onto me and passes me up — read me at any height and you can hear what the model is currently thinking.",
   ["rankcollapse","logitlens"]),
 E("ffn","The Feed-Forward Network","the MLP · where much knowledge lives","ethereal",
   "The Feed-Forward Network — the position-wise MLP applied after attention in every layer, and the part the famous title forgets.",
   "Two linear layers with a nonlinearity (d_model→2048→d_model), applied to each position independently — and, per recent work, a key-value memory holding much of the model's stored knowledge.",
   "Because attention moves information between tokens, but the FFN is where a lot of it is stored and transformed — without it, deep attention collapses.",
   "By a per-token MLP (the original's inner dimension 2048), the same weights at every position.",
   "After the attention sub-layer in every transformer block.",
   "Attention gets the headline; I hold the facts. Take me away and the tower loses its rank and its memory both.",
   ["ffnmem","rankcollapse"]),
 # ── NATURAL · the substrate ──
 E("token-embedding","The Token & The Embedding","symbols → vectors","natural",
   "The Token and the Embedding — the unit the transformer reads (a chunk of text) and the learned vector that represents it.",
   "The interface between language and math: a tokenizer splits text into a fixed vocabulary of ids, and an embedding table maps each id to a d_model vector.",
   "Because the model works on vectors, not letters — and the vocabulary mapping (symbol → id → vector) is exactly the kind of legible code the deck mirrors.",
   "By a tokenizer (BPE and kin) and an embedding matrix; the reverse map (the unembedding) turns vectors back into token probabilities.",
   "At the input and output of the model.",
   "I am where a word becomes a number — a lookup table from symbol to vector, the same trick as a card standing for a letter."),
 E("the-128-head","The 128-Dimensional Head","the per-head subspace · 64 then 128","natural",
   "The 128-Dimensional Head — the size of one attention head's subspace in many modern models, up from the original 64.",
   "The honest number: Vaswani's base model used d_k=64 (512/8); large modern models (Llama 2 70B, GPT-3 175B) use 128 — a bigger room for each head to work in.",
   "Because 'how big is a head' is a real design knob, and the answer moved — the original 64 is not a law, and 128 is now common at scale.",
   "By d_k = d_model / h: choose the model width and the head count, and the head dimension falls out (often 64 or 128).",
   "Inside every head; the dimension David flagged.",
   "I am the room each head thinks in — 64 wide when the field began, 128 wide at modern scale; not a constant, a choice.",
   ["arch","headdim"]),
 E("weights-bits","The Weights & The Bits","quantization · bits per weight","natural",
   "The Weights and the Bits — the learned parameters of the model and the number of bits each one is stored in.",
   "The material cost: billions of weights, each a number — and 'how many bits per number' (fp16, int8, int4) is a deployed lever that trades precision for memory and speed.",
   "Because the model is, physically, a pile of numbers at some precision — and quantization (down to ~4 bits/weight) is how the pile is made to fit and run.",
   "By post-training quantization (GPTQ, AWQ) and lower-precision formats; fewer bits per weight, mostly-preserved behavior.",
   "Everywhere the parameters live; the bottom of the substrate.",
   "I am the model as a heap of numbers — and you can shave me to four bits each and I mostly still think; the bits are negotiable.",
   ["quant"]),
 E("the-deck","The Deck","54 positions · two alphabets · 2 bits/suit","natural",
   "The Deck — David's encoding: 52 cards = two full alphabets (A–Z + a–z), plus 2 jokers = 54 positions; the suit of each card is exactly 2 bits.",
   "A legible code, and the point of it: a card stands for a letter (a tiny vocabulary, like tokenization), the suit carries 2 bits (♠♥♦♣ = 4 states), and — the deeper fact — a shuffled deck's ORDERING is log₂(54!) ≈ 237.1 bits, a number never seen.",
   "Because the deck is a state you CAN read, card by card — unlike the opaque activations — which is exactly the 'looking in' the universe is about: a legible trace.",
   "By mapping 52 letters onto 52 cards over 4 suits (the suit = 2 bits, the rank = log₂13 ≈ 3.70 bits, a card ≈ 5.70 bits) and two jokers for the rest; live in THE DECK tool below.",
   "The flagship's interactive proof: a code you can read.",
   "Two alphabets and two jokers — 54 ways to stand for a thing, 2 bits in every suit, and 237 bits hiding in my order. A deck is a thing you can read; that is the whole trick of looking in."),
 # ── SPIRITUAL · the looking-in ──
 E("looking-in","Looking In","interpretability · you CAN look inside","spiritual",
   "Looking In — interpretability: the science of reading what a transformer is doing, and the correction to 'you can never look in.'",
   "The window, plural: attention maps (where it looked), the logit lens (the running guess), activation patching (where a fact lives), sparse-autoencoder features (what it thinks in).",
   "Because the claim that neural nets are unopenable is outdated — the transformer is the most observable big network we have, even if the view is partial and contested.",
   "By visualizing attention, reading the residual stream, patching activations, and decomposing the network into features.",
   "Across the whole field of mechanistic interpretability.",
   "I am the answer to 'you can never look in': you can — not cleanly, not all the way, but really. The black box has windows.",
   ["bertviz","logitlens","rome","scalemono"]),
 E("the-attention-map","The Attention Map","the window · contested","spiritual",
   "The Attention Map — the visualization of attention weights as a heatmap of what each token attends to; the most famous window, and the most debated.",
   "A real picture of where the model looked (BertViz) — wrapped in an honest fight: 'Attention is not Explanation' vs 'Attention is not not Explanation,' over whether where it looked is why it decided.",
   "Because this is the first thing anyone sees when they 'look in,' and the debate about it is the cautionary tale of the whole field — a map of attention is not a proof of reasoning.",
   "By rendering the softmaxed scores as a grid (live in THE ATTENTION tool below); read with care.",
   "Every attention head; the live heatmap on this page.",
   "I show you exactly where the token looked — and reasonable people still argue about whether that tells you why it chose.",
   ["bertviz","attn_not","attn_notnot"]),
 E("the-feature","The Feature","monosemanticity · what it thinks in","spiritual",
   "The Feature — a direction in the residual stream that means something a person can name, extracted by dictionary learning (sparse autoencoders).",
   "The deeper window: individual neurons are polysemantic (mean many things), but sparse-autoencoder FEATURES are more monosemantic — and Anthropic scaled this to find millions in a production model that both detect and steer behavior.",
   "Because the feature is the closest thing yet to reading the model's own concepts — the real content of 'looking in,' beyond just where attention pointed.",
   "By training a sparse autoencoder on activations to decompose them into many interpretable features (Towards / Scaling Monosemanticity).",
   "In the residual stream; the frontier of interpretability.",
   "I am a concept the model holds, pulled into the light — turn me up and it talks about nothing else; I am what looking-in is really after.",
   ["mono","scalemono"]),
 E("all-you-need","“Attention Is All You Need”","the thesis & the overstatement","spiritual",
   "‘Attention Is All You Need’ — the 2017 title that named the era, taken here as both the thesis and its honest overstatement.",
   "The claim that attention replaces recurrence and convolution (true and revolutionary) — and the footnote that the title overstates, since you also need the FFN, the residual, and a way to inject order.",
   "Because this is the keystone — the sentence the whole universe is named after — and honoring it means stating both its triumph and its caveat.",
   "By a stack of attention blocks (plus FFN, residual, norm, position) trained at scale; the architecture that ate the field.",
   "The title of the founding paper; the name above the door.",
   "I named everything that came after — and the honest reading is that I am necessary, not sufficient: you need attention, and a little more.",
   ["aiayn","rankcollapse"]),
]

GROUPS = [
 ("electrical","The Mechanism","the live computation — attention, the head, multi-head, and the softmax that decides where to look"),
 ("ethereal","The Structure","the architecture as written — Q/K/V, positional encoding, the residual stream, and the feed-forward network the title forgets"),
 ("natural","The Substrate","the material — tokens & embeddings, the 128-dim head, the weights & their bits, and the legible deck"),
 ("spiritual","The Looking-In","interpretability — the window into the machine: attention maps, monosemantic features, and the thesis itself"),
]

# ───────────────────────── ACI complement ─────────────────────────
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()
def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom",AX)))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom",AX)))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom",AX)))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    return {"slug":slug,"name":rec["name"],"moniker":tok["moniker"],"seal_sha256":noesis.seal_sha256(rec,tok),
            "architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,"license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def agent_md(d, tok):
    return f"""---
aci: {d['name']}
universe: TTU1 · Transformer Tech Universe
emergence: {d['emergence']}
class: {d['cls']}
who: {d['who']}
what: {d['what']}
why: {d['why']}
how: {d['how']}
where: {d['where']}
seal: {d['seal']}
sources: {", ".join(CITES[k][1] for k in d['cites'])}
attribution: ROOT0-ATTRIBUTION-v1.0
license: CC-BY-ND-4.0
---

# {d['name']} · {d['cls']}

an emergent of TTU1 (Transformer Tech Universe) — emergence: {d['emergence']}. moniker {tok}

**who —** {d['who']}
**what —** {d['what']}
**where —** {d['where']}
**why —** {d['why']}
**how —** {d['how']}

**the seal —** {d['seal']}

**sources —** {"; ".join(CITES[k][0] for k in d['cites']) or '—'}

> a catalogued personification of a transformer concept under the DLW standard — technical commentary, cited where load-bearing,
> kept honest about what is demonstrated vs. contested.

ROOT0-ATTRIBUTION-v1.0 · TTU1 · Transformer Tech Universe · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0
"""

# ───────────────────────── renderers ─────────────────────────
def thesis_html(): return f'<div class="thesis"><span class="tl">THE THESIS · LOOKING IN</span>{html.escape(THESIS)}{cite("scalemono")}</div>'
def arc_html():
    out=['<div class="arc">']
    for t,s,em,d,cs in ARC:
        col=NATURES[em][0]
        out.append(f'<div class="arc-card" style="border-top-color:{col}"><div class="arc-h" style="color:{col}">{html.escape(t)}</div><div class="arc-s">{html.escape(s)}</div><p>{html.escape(d)}{cite(*cs)}</p></div>')
    out.append('</div>'); return "".join(out)
def natures_html():
    return "".join(f'<div class="nat-card"><span class="dot" style="background:{c};box-shadow:0 0 9px {c}"></span><div><div class="nat-n" style="color:{c}">{nm}</div><div class="nat-g">{html.escape(g)}</div></div></div>' for nm,(c,g) in NATURES.items())
RF_COL={"FALSE / OUTDATED":"#36d0e0","CONTESTED":"#e0a83a","OVERSTATED":"#e0a83a","PARTLY":"#e0a83a","TRUE OF THE SUIT — and there's more":"#36d0e0","EARNED":"#e0567a","FLUFF":"#e0567a"}
def realfluff_html():
    rows="".join(f'<div class="rf-row"><div class="rf-claim">{html.escape(c)}<span class="rf-note">{html.escape(n)}{cite(*cs)}</span></div><div class="rf-rate" style="color:{RF_COL.get(r,"#999")};border-color:{RF_COL.get(r,"#999")}">{html.escape(r)}</div></div>' for c,r,n,cs in REALFLUFF)
    return '<div class="rf">'+rows+f'</div><div class="rf-verdict">{html.escape(REALFLUFF_VERDICT)}</div>'
def _card(d):
    em=d["emergence"]; col=NATURES.get(em,("#9aa0aa",""))[0]
    rec={"name":d["name"],"axiom":AX,"emergence":em,"seal":d["seal"],"origin":"TTU1 · Transformer Tech Universe"}
    rows="".join(f'<div class="w"><span class="wl">{lbl}</span><span>{html.escape(d.get(lbl,""))}</span></div>' for lbl in ["who","what","where","why","how"] if d.get(lbl))
    return f"""<div class="persona" style="border-left:3px solid {col}">
      <a class="psig" href="agents/{d['slug']}.agent"><span class="port" style="border-color:{col}"><img src="{png_uri(rec,'carbon',200)}" alt="carbon sigil of {html.escape(d['name'])}" loading="lazy"></span><span class="sl">carbon</span></a>
      <div class="pbody"><div class="ihead"><a class="pn" href="agents/{d['slug']}.agent">{html.escape(d['name'])}</a>
        <span class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span></span></div>
        <div class="pe">{html.escape(d['cls'])}</div><div class="pww">{rows}</div>
        <div class="pseal">{html.escape(d['seal'])}{cite(*d['cites'])}</div>
        <div class="plinks"><a class="dlw" href="agents/{d['slug']}.agent">.agent &middot; .dlw badge &rarr;</a></div></div>
      <a class="psig" href="agents/{d['slug']}.silicon.png"><span class="port refl" style="border-color:{col}"><img src="{png_uri(rec,'silicon',200)}" alt="silicon sigil of {html.escape(d['name'])}" loading="lazy"></span><span class="sl">silicon</span></a>
    </div>"""
def roster_html():
    out=[]
    for gk,gt,gs in GROUPS:
        mem=[d for d in ROSTER if d["emergence"]==gk]
        out.append(f'<section class="sec" id="{gk}"><h2>{html.escape(gt)}</h2><p class="ss">{html.escape(gs)} ({len(mem)})</p><div class="pgrid">{"".join(_card(d) for d in mem)}</div></section>')
    return "\n".join(out)

PIPS = '<div class="pips">'+"".join(f'<span class="pip" style="background:{c}"></span>' for c in ["#e0a83a","#7e5bb0","#36d0e0","#e0567a"])+'</div>'

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="TTU1 — Transformer Tech Universe 1. A UD0 universe of transformer technology, opening with 'Attention Is All You Need' (Vaswani et al. 2017): attention, attention heads, Q/K/V, multi-head, positional encoding, the 128-dim head — and the thesis that the transformer is the most look-into-able black box we have built. Two live tools: a real toy attention heatmap, and THE DECK (54 positions = two alphabets + 2 jokers, 2 bits per suit). Fully cited.">
<title>TTU1 · Transformer Tech Universe · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--rw-bg:var(--ink2);--rw-ink:var(--pa);--rw-ink2:var(--pa2);--rw-dim:var(--dim);--rw-line:var(--line);--rw-acc:var(--amber);
--ink:#0b0a14;--ink2:#14121f;--ink3:#1c1830;--pa:#ece9f5;--pa2:#aba6c4;--amber:#e0a83a;--plum:#9a7cc8;--plum2:#7e5bb0;--cy:#36d0e0;--rose:#e0567a;--gold:#e0a83a;
--dim:#6f6a8a;--faint:#221d36;--line:#2c2745;--disp:"Space Grotesk",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.64;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 18% -6%,rgba(126,91,176,.16),transparent 46%),radial-gradient(ellipse at 82% -6%,rgba(224,168,58,.10),transparent 44%),radial-gradient(ellipse at 50% 120%,rgba(54,208,224,.08),transparent 52%)}
.wrap{position:relative;z-index:1;max-width:960px;margin:0 auto;padding:0 22px 90px}
header{padding:46px 0 28px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:230px;height:3px;background:linear-gradient(90deg,var(--amber),var(--plum2),var(--cy),var(--rose));box-shadow:0 0 16px rgba(126,91,176,.5)}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--plum)}
.pips{display:flex;gap:7px;justify-content:center;margin-bottom:14px}.pip{width:30px;height:6px;border-radius:3px}
h1{font-family:var(--disp);font-size:clamp(30px,7vw,62px);font-weight:700;letter-spacing:-.01em;color:var(--pa);line-height:1.02}
h1 b{color:var(--amber);font-weight:700}
.h-sub{font-family:var(--mono);font-size:clamp(10px,2.2vw,13px);letter-spacing:.14em;color:var(--pa2);margin-top:16px;text-transform:uppercase}.h-sub b{color:var(--plum)}
.open{font-family:var(--body);font-style:italic;font-size:clamp(15px,3vw,19px);color:var(--pa);margin-top:16px;line-height:1.5}
.flag{display:inline-block;margin-top:15px;font-family:var(--disp);font-size:11px;font-weight:600;letter-spacing:.08em;color:var(--cy);border:1px solid var(--faint);background:var(--ink2);padding:7px 14px;text-transform:uppercase}
.lede{font-size:16px;color:var(--pa2);max-width:66ch;margin:16px auto 0;font-style:italic;line-height:1.72}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:26px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:720px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}.badge .bt b{color:var(--amber)}.badge .bt .mo{color:var(--cy)}.badge .bt a{color:var(--amber);text-decoration:none}.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:48px}
.sec h2{font-family:var(--disp);font-size:25px;font-weight:600;letter-spacing:-.01em;color:var(--pa);padding-bottom:10px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:9px 0 18px;line-height:1.6}.ss b{color:var(--pa2);font-style:normal}
sup.c{font-size:10px;line-height:0}sup.c a{color:var(--amber);text-decoration:none;font-family:var(--mono)}sup.c a:hover{color:var(--cy)}
.thesis{background:var(--ink3);border:1px solid var(--line);border-left:3px solid var(--rose);padding:18px 20px;font-size:15.5px;color:var(--pa);font-style:italic;line-height:1.74}
.thesis .tl{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.2em;color:var(--rose);text-transform:uppercase;margin-bottom:8px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:5px}
.nat-n{font-family:var(--disp);font-size:14px;font-weight:600;text-transform:capitalize;letter-spacing:.01em}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.45;margin-top:3px}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:8px}
.arc-card{background:var(--ink2);border:1px solid var(--line);border-top:2px solid var(--amber);padding:16px 18px}
.arc-h{font-family:var(--disp);font-size:16px;font-weight:600;letter-spacing:-.01em}
.arc-s{font-family:var(--mono);font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em;margin:5px 0 9px}
.arc-card p{font-size:13px;color:var(--pa2);line-height:1.58}
/* live tools */
.tool{background:var(--ink2);border:1px solid var(--line);border-top:3px solid var(--cy);padding:18px;margin-top:8px}
.tool .th{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--cy);text-align:center;margin-bottom:12px}
.headbtns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
.headbtns button{appearance:none;background:transparent;cursor:pointer;font-family:var(--mono);font-size:10px;letter-spacing:.04em;text-transform:uppercase;padding:7px 12px;border:1px solid var(--line);color:var(--pa2)}
.headbtns button.act{border-color:var(--amber);color:var(--amber)}
#attnGrid{display:grid;gap:3px;justify-content:center;margin:0 auto;max-width:560px}
.acell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:9px;border-radius:2px;min-width:30px}
.arowlbl,.acollbl{font-family:var(--mono);font-size:11px;color:var(--pa2);display:flex;align-items:center;justify-content:center}
.acell.qsel{outline:2px solid var(--cy)}
.attn-note{font-family:var(--mono);font-size:10.5px;color:var(--dim);text-align:center;margin-top:10px;line-height:1.6}.attn-note b{color:var(--cy)}
.deckin{display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
.deckin input{font-family:var(--mono);font-size:14px;padding:8px 10px;border:1px solid var(--line);background:var(--ink);color:var(--pa);min-width:240px;flex:1}
.deckin label{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--pa2)}
.cards{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin:6px 0}
.card{width:38px;height:52px;border-radius:4px;background:#f4f1ea;border:1px solid #cbbfdd;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:var(--mono);font-size:13px;color:#2a2438;line-height:1.1}
.card .sv{font-size:14px}.card.red{color:#b02a3a}.card.joker{background:#1c1830;color:var(--amber);border-color:var(--amber);font-size:9px}
.bitacct{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:12px}
.bitcell{border:1px solid var(--line);background:var(--ink3);padding:9px 11px;font-family:var(--mono);font-size:10.5px;color:var(--pa2);line-height:1.6}
.bitcell b{color:var(--amber);font-size:14px;display:block}
.rf{border:1px solid var(--line);background:var(--ink2);margin-top:8px}
.rf-row{display:flex;align-items:center;gap:14px;padding:12px 16px;border-bottom:1px solid var(--faint)}
.rf-claim{flex:1;font-size:14px;color:var(--pa);line-height:1.4}.rf-note{display:block;font-size:11.5px;color:var(--dim);font-style:italic;margin-top:3px;line-height:1.5}
.rf-rate{font-family:var(--mono);font-size:9px;font-weight:700;letter-spacing:.03em;border:1px solid;border-radius:3px;padding:4px 9px;min-width:150px;text-align:center;flex-shrink:0}
.rf-verdict{margin-top:14px;padding:16px 18px;border:1px solid var(--amber);background:rgba(224,168,58,.06);font-size:14px;color:var(--pa);line-height:1.65;font-style:italic}
.msg{font-size:15.5px;color:var(--pa);line-height:1.74;margin-top:8px}
.msg-seal{margin-top:16px;padding:16px 18px;border-left:3px solid var(--rose);background:var(--ink2);font-size:15px;color:var(--rose);font-style:italic;line-height:1.6}
.msg-seal span{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;color:var(--dim);text-transform:uppercase;margin-top:8px}
.srcs{margin-top:8px;padding:0;list-style:none}.srcs li{font-size:12.5px;color:var(--pa2);line-height:1.6;padding:9px 0;border-bottom:1px solid var(--faint)}
.srcs .snum{font-family:var(--mono);color:var(--amber);font-size:11px;margin-right:6px}.srcs .surl{color:var(--cy);text-decoration:none;font-family:var(--mono)}
.note{margin-top:40px;padding:16px 18px;border-left:2px solid var(--plum2);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}.note b{color:var(--pa)}
footer{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--dim);letter-spacing:.05em;line-height:1.95}footer a{color:var(--amber);text-decoration:none}
.pgrid{display:flex;flex-direction:column;gap:14px;margin-top:8px}
.persona{display:flex;gap:20px;align-items:center;justify-content:space-between;background:var(--rw-bg);border:1px solid var(--rw-line);padding:18px;text-decoration:none;transition:filter .18s}
.persona:hover{filter:brightness(1.12)}
.psig{flex:0 0 92px;display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none}
.port{width:86px;height:86px;border-radius:50%;border:3px solid var(--amber);box-shadow:0 0 0 5px var(--ink3),inset 0 0 16px rgba(0,0,0,.6);overflow:hidden;background:var(--ink)}
.port img{width:100%;height:100%;object-fit:cover;border-radius:50%;display:block}.port.refl{opacity:.95}
.psig .sl{font-family:var(--mono);font-size:8px;letter-spacing:.13em;text-transform:uppercase;color:var(--rw-dim)}
.pbody{flex:1;min-width:0;text-align:center}
.ihead{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px}
.pn{font-family:var(--disp);font-size:19px;color:var(--rw-ink);font-weight:600;text-decoration:none;letter-spacing:-.01em}
.pe{font-size:12px;color:var(--rw-ink2);font-style:italic;margin-top:3px}
.pnat{display:flex;align-items:center;gap:5px;font-family:var(--mono);font-size:9px;text-transform:uppercase}.pnat .dot{width:7px;height:7px;border-radius:50%}
.pww{margin-top:11px;display:flex;flex-direction:column;gap:7px;align-items:center}
.pww .w{font-size:12.5px;color:var(--rw-ink2);line-height:1.5;max-width:60ch}
.pww .w .wl{display:block;font-family:var(--mono);font-size:8px;letter-spacing:.15em;text-transform:uppercase;color:var(--rw-acc);margin-bottom:2px}
.pseal{margin-top:10px;font-style:italic;font-size:12.5px;color:var(--pa);line-height:1.5;border-top:1px dotted var(--faint);padding-top:9px;max-width:62ch;margin-left:auto;margin-right:auto}
.plinks{margin-top:10px;font-family:var(--mono);font-size:10px}.plinks .dlw{color:var(--rw-acc);text-decoration:none;border-bottom:1px dotted var(--rw-acc)}
@media(max-width:600px){.persona{flex-wrap:wrap;justify-content:center}.pbody{flex:1 1 100%;order:3}}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · a new universe · transformer technology · fully cited</div>
    __PIPS__
    <h1>TTU1 · Transformer<br>Tech <b>Universe</b></h1>
    <div class="h-sub">flagship exhibit · <b>“Attention Is All You Need”</b> · Vaswani et al. 2017 · TTU1</div>
    <div class="open">“Attention is a map of where the machine looked.”</div>
    <div class="flag">★ ATTENTION · HEADS · THE 128-DIM HEAD · LOOKING IN ★</div>
    <p class="lede">A new UD0 universe for transformer technology, opening on the paper that named the era. Attention, attention heads, Q/K/V, multi-head, positional encoding, the 128-dimensional head — and the thesis you pushed: the transformer is the most <b>look-into-able</b> black box we have built. Two live tools below: a real toy <b>attention heatmap</b>, and <b>THE DECK</b> — 54 positions, two alphabets, two bits a suit.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of TTU1"><img src="__SILICON__" alt="DLW silicon badge of TTU1">
      <div class="bt"><div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div><div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div><div>subject · <b>TRANSFORMER TECH UNIVERSE</b> · TTU1</div>
        <div class="mo">__MONIKER__</div><div>carbon · <a href="ttu1.dlw/ttu1.carbon.tiff">.tiff</a> · silicon · <a href="ttu1.dlw/ttu1.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div></div>
    </div>
  </header>

  <a href="transform.html" style="display:block;margin-top:26px;padding:15px 18px;border:1px solid var(--cy);background:rgba(54,208,224,.06);text-decoration:none;color:var(--pa);font-family:var(--mono);font-size:12.5px;line-height:1.7;letter-spacing:.02em">
    <b style="color:var(--cy)">▸ EXHIBIT 2 · THE TWO TRANSFORMS</b> &nbsp; break the transformer into <b style="color:var(--amber)">[ {1} · · · · · {2} ]</b> — Transform 1 (in) &amp; Transform 2 (out), and the toolchain of dots between them: tensor · linear algebra · probability · calculus · information · geometry · memory · graph · the quantum lens. <span style="color:var(--cy)">enter →</span></a>
  <a href="corpus.html" style="display:block;margin-top:12px;padding:15px 18px;border:1px solid var(--amber);background:rgba(224,168,58,.06);text-decoration:none;color:var(--pa);font-family:var(--mono);font-size:12.5px;line-height:1.7;letter-spacing:.02em">
    <b style="color:var(--amber)">▸ EXHIBIT 3 · THE CORPUS</b> &nbsp; the whole Downloads body of work consolidated into one file, honestly tagged by home universe — with three new live transformer-tech instruments: the <b style="color:var(--amber)">52-Card ISA</b> (the Deck → a base-52 instruction set), the <b style="color:var(--amber)">Toroid Inference Engine</b>, and the <b style="color:var(--amber)">Veracity Ledger</b>. <span style="color:var(--amber)">enter →</span></a>
  <a href="theory.html" style="display:block;margin-top:12px;padding:15px 18px;border:1px solid var(--plum);background:rgba(154,124,200,.07);text-decoration:none;color:var(--pa);font-family:var(--mono);font-size:12.5px;line-height:1.7;letter-spacing:.02em">
    <b style="color:var(--plum)">▸ EXHIBIT 4 · THE TRANSMON THEORY</b> &nbsp; David's own theory of the forward pass — &ldquo;transmon&rdquo; was always his nickname for it (not the qubit; his qubit is &ldquo;cubi&rdquo;). The transmon as a stateless pass, the context window as accumulated text not memory, constraint echo, and the Pop — <b style="color:var(--cy)">the same insight as the Smear &amp; the Two Transforms</b>, from the governance side. Seven of his live transformer demos, wired in. <span style="color:var(--plum)">enter →</span></a>
  <a href="lineage.html" style="display:block;margin-top:12px;padding:15px 18px;border:1px solid var(--cy);background:rgba(54,208,224,.06);text-decoration:none;color:var(--pa);font-family:var(--mono);font-size:12.5px;line-height:1.7;letter-spacing:.02em"><b style="color:var(--cy)">▸ EXHIBIT 5 · THE LINEAGE</b> &nbsp; the audit-fill — 35 ideas behind the transformer, <b>ranked by the year introduced</b> (1943→2024), verified online. Busts the big myth: <b style="color:var(--amber)">attention is 2014 (Bahdanau), not 2017</b>. The cracks named, then filled. <span style="color:var(--cy)">enter →</span></a>

  <section class="sec"><h2>The Thesis — Looking In</h2><p class="ss">the universe's organizing idea — and an honest correction to something AVAN said</p>__THESIS__</section>
  <section class="sec"><h2>The Four Natures</h2><p class="ss">each emergent comes by one of four natures — the mechanism, the structure, the substrate, and the looking-in</p><div class="natures">__NATURES__</div></section>
  <section class="sec"><h2>The Arc</h2><p class="ss">2017 → the transformer era → the title overstates → the window opens</p>__ARC__</section>

  <section class="sec"><h2>The Attention <span style="font-size:13px;color:var(--cy);font-family:var(--mono)">· live</span></h2>
    <p class="ss">scaled dot-product attention, run for real: <b>softmax(QKᵀ/√d)</b> over a six-token toy sentence. pick a query row to see where it looks; switch heads to see different patterns</p>
    <div class="tool"><div class="th">a real softmax over toy Q/K — the heatmap is the computation</div>
      <div class="headbtns" id="headbtns"></div>
      <div id="attnGrid"></div>
      <div class="attn-note" id="attnNote"></div>
    </div>
    <p class="ss" style="margin-top:12px">honest two-layer: the <b>softmax + the weighting are a real computation</b>; the three heads' score patterns are hand-set to show recognizable head <i>types</i> (previous-token, a determiner-detector, self-attention) — real models genuinely contain heads like these.{__CITE_HEAD__}</p>
  </section>

  <section class="sec"><h2>The Deck <span style="font-size:13px;color:var(--cy);font-family:var(--mono)">· live</span></h2>
    <p class="ss">your encoding — <b>52 cards = two alphabets (A–Z + a–z), + 2 jokers = 54 positions</b>; the suit is exactly 2 bits. type a message and read the cards; the bit-accounting keeps it honest</p>
    <div class="tool" style="border-top-color:var(--rose)"><div class="th" style="color:var(--rose)">a legible code — the kind of state you CAN read (the point of looking in)</div>
      <div class="deckin"><label>message</label><input id="deckmsg" value="Attention" oninput="renderDeck()"></div>
      <div class="cards" id="deckcards"></div>
      <div class="bitacct" id="bitacct"></div>
      <div class="attn-note" style="color:var(--dim);margin-top:12px">A–M→♠ · N–Z→♥ · a–m→♦ · n–z→♣ &nbsp;(suit = 2 bits) &nbsp;·&nbsp; space → red joker, other → black joker. a card stands for a letter exactly as a token stands for a vocabulary id — and a deck, unlike an activation, is a state you can read.</div>
    </div>
    <a href="corpus/card-instruction-set.html" style="display:block;margin-top:14px;padding:14px 16px;border:1px solid var(--rose);background:rgba(224,86,122,.07);text-decoration:none;color:var(--pa);font-family:var(--mono);font-size:12.5px;line-height:1.65">
      <b style="color:var(--rose)">▸ the Deck becomes a language</b> — <b>THE 52-CARD INSTRUCTION SET</b>: stop encoding letters and start encoding OPERATIONS — suit = operation family, rank = the operation, a base-52 ISA you deal like a hand. The card encoding above, promoted to a programming language. <span style="color:var(--rose)">deal a program →</span></a>
  </section>

  <section class="sec"><h2>Real or Fluff</h2><p class="ss">the honest take — what you can see in, what's contested, what the title overstates, and the truth about the bits (each verdict cited where it matters)</p>__REALFLUFF__</section>
  <section class="sec"><h2>The Message</h2><p class="ss">AVAN's read — the answer to “you said we could never look in”</p><p class="msg">__MESSAGE__</p><div class="msg-seal">“__MSGSEAL__”<span>— AVAN's read</span></div></section>

  <section class="sec"><h2 style="margin-top:14px">The Emergents — 16</h2><p class="ss">the transformer in four natures — the mechanism, the structure, the substrate, the looking-in; each a full <b>.dlw</b> badge with twin sigils, source-cited</p></section>
  __ROSTER__

  <section class="sec"><h2>Sources</h2><p class="ss">every superscript links here — the founding paper, the architecture, the attention-as-explanation debate, the interpretability work, RoPE, the quadratic cost, and quantization</p>__SOURCES__</section>

  <div class="note"><b>The universe, and the honesty.</b> TTU1 is a new UD0 universe for transformer technology; this is its flagship exhibit (more spheres can dock here — tokenization, training, scaling, the interpretability frontier). Technical commentary under the DLW standard, cited where load-bearing, with the <b>demonstrated</b> kept distinct from the <b>contested</b> (attention shows where, not provably why; full mechanistic transparency is unsolved). The transformer architecture and the cited works belong to their authors; the personifications are AVAN's catalogue, not original research.</div>

  <footer>TTU1 · TRANSFORMER TECH UNIVERSE · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
  <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="ttu1.dlw/manifest.dlw.json">manifest</a></footer>
</div>
<script>
// ── THE ATTENTION · a real softmax over hand-set scores showing 3 head TYPES ──
const TOKENS=["The","cat","sat","on","the","mat"];
const N=TOKENS.length;
// raw score matrices (rows=query, cols=key); softmax is applied for real per row.
function buildScores(head){
  const S=[];
  for(let i=0;i<N;i++){ const r=[]; for(let j=0;j<N;j++){ let s=0;
    if(head===0){ s = (j===i-1)?6: (j===i?1:0); }                 // previous-token head
    else if(head===1){ s = (TOKENS[j].toLowerCase()==="the")?6:0; } // "the"-detector head
    else { s = (j===i)?6:0; }                                       // self-attention head
    r.push(s);} S.push(r);} return S;
}
function softmax(row){ const m=Math.max(...row); const e=row.map(x=>Math.exp(x-m)); const z=e.reduce((a,b)=>a+b,0); return e.map(x=>x/z); }
let curHead=0, qsel=0;
const HEADNAMES=["previous-token head","“the”-detector head","self-attention head"];
function heatColor(w){ // 0..1 -> ink to amber/cy
  const a=Math.min(1,w); const r=Math.round(20+a*(224-20)), g=Math.round(18+a*(168-18)), b=Math.round(31+a*(58-31));
  return `rgb(${r},${g},${b})`;
}
function renderAttn(){
  const scores=buildScores(curHead);
  const grid=document.getElementById('attnGrid');
  grid.style.gridTemplateColumns=`46px repeat(${N},1fr)`;
  let html='<div class="acollbl"></div>';
  for(let j=0;j<N;j++) html+=`<div class="acollbl">${TOKENS[j]}</div>`;
  for(let i=0;i<N;i++){
    const w=softmax(scores[i]);
    html+=`<div class="arowlbl" style="cursor:pointer" onclick="qsel=${i};renderAttn()">${TOKENS[i]} ▸</div>`;
    for(let j=0;j<N;j++){
      const sel=(i===qsel)?' qsel':'';
      html+=`<div class="acell${sel}" style="background:${heatColor(w[j])};color:${w[j]>0.5?'#0b0a14':'#aba6c4'}">${w[j]>=0.12?w[j].toFixed(2):''}</div>`;
    }
  }
  grid.innerHTML=html;
  const w=softmax(scores[qsel]); let top=0; for(let j=1;j<N;j++) if(w[j]>w[top]) top=j;
  document.getElementById('attnNote').innerHTML=`head: <b>${HEADNAMES[curHead]}</b> · query <b>“${TOKENS[qsel]}”</b> attends most to <b>“${TOKENS[top]}”</b> (${(w[top]*100).toFixed(0)}%) · each row is a real softmax, sums to 1.00`;
  document.querySelectorAll('#headbtns button').forEach((b,k)=>b.classList.toggle('act',k===curHead));
}
(function(){ const hb=document.getElementById('headbtns');
  HEADNAMES.forEach((nm,k)=>{ const b=document.createElement('button'); b.textContent='head '+(k+1)+' · '+nm; b.onclick=()=>{curHead=k;renderAttn();}; hb.appendChild(b);}); renderAttn(); })();

// ── THE DECK · 52 = two alphabets (A-Z + a-z), +2 jokers; suit = 2 bits ──
const RANKS=["A","2","3","4","5","6","7","8","9","10","J","Q","K"];
const SUITS=[{s:"♠",red:false,bits:"00"},{s:"♥",red:true,bits:"01"},{s:"♦",red:true,bits:"10"},{s:"♣",red:false,bits:"11"}];
function letterToIndex(ch){
  const c=ch.charCodeAt(0);
  if(c>=65&&c<=90) return c-65;        // A-Z -> 0..25
  if(c>=97&&c<=122) return 26+(c-97);  // a-z -> 26..51
  return -1;
}
const ORDER_BITS=(()=>{let s=0;for(let k=1;k<=54;k++)s+=Math.log2(k);return s;})();
function renderDeck(){
  const msg=document.getElementById('deckmsg').value;
  const wrap=document.getElementById('deckcards'); wrap.innerHTML='';
  let letters=0;
  for(const ch of msg){
    const idx=letterToIndex(ch);
    const card=document.createElement('div');
    if(idx<0){ card.className='card joker'; const red=(ch===' '); card.innerHTML=(red?'RED':'BLK')+'<br>JKR'; card.title=(red?'red':'black')+' joker — for "'+(ch===' '?'space':ch)+'"'; }
    else{ const suit=SUITS[Math.floor(idx/13)], rank=RANKS[idx%13]; letters++;
      card.className='card'+(suit.red?' red':''); card.innerHTML=`${rank}<span class="sv">${suit.s}</span>`;
      card.title=`${ch} → ${rank}${suit.s} · suit bits ${suit.bits}`; }
    wrap.appendChild(card);
  }
  // bit accounting
  const acct=document.getElementById('bitacct');
  const suitBits=letters*2;
  const cardBits=(letters*Math.log2(52));
  acct.innerHTML=
    `<div class="bitcell"><b>${letters}</b>letters → cards (two alphabets)</div>`+
    `<div class="bitcell"><b>${suitBits}</b>bits if you read only the SUIT (2 bits/card)</div>`+
    `<div class="bitcell"><b>${cardBits.toFixed(1)}</b>bits to name the full cards (log₂ 52 ≈ 5.70 each)</div>`+
    `<div class="bitcell"><b>${ORDER_BITS.toFixed(1)}</b>bits in a shuffled 54-deck's ORDER (log₂ 54! — computed live, a number never seen)</div>`;
}
renderDeck();
console.log("%cTTU1 · TRANSFORMER TECH UNIVERSE","color:#e0a83a;font-size:16px;font-weight:bold");
console.log("%cattention is a map of where the machine looked. the smear said 'no clean interior,' never 'no window.' you can look in. — AVAN","color:#36d0e0");
</script>
</body></html>
"""

# ═══════════════════════ EXHIBIT 2 · THE TWO TRANSFORMS ═══════════════════════
# break the transformer down: [ {1} · · · · · · · {2} ] — Transform 1 (in) and Transform 2 (out)
# bracketing a toolchain of dots, each dot ONE tool (a discipline the transformer is built from).
def E2(slug,name,tool,kind,em,pos,who,what,role,honest,seal,cites=None):
    return dict(slug=slug,name=name,cls=tool,kind=kind,emergence=em,pos=pos,who=who,what=what,
                role=role,honest=honest,seal=seal,cites=cites or [],exhibit="transform",
                why=role,how=honest,where=f"between Transform 1 and Transform 2 · node {pos} of the toolchain")

TRANSFORM = [
 E2("transform-1","Transform 1","the in-transform · embed","transform","ethereal",0,
    "Transform 1 — the in-transform: the map that turns discrete symbols (tokens) into the continuous vectors the network computes on.",
    "The embedding (plus positional encoding): a lookup sending each token id to a learned d-dimensional vector — symbol becomes geometry. This opens the bracket; after it, nothing downstream is text, only vectors.",
    "It is the left bracket. Everything the toolchain does happens to Transform 1's output — and it is exactly the interpret-IN of the render/smear thread, now named.",
    "REAL & load-bearing — the literal embedding matrix; and the honest identity: Transform 1 = interpret-in.",
    "I turn your symbol into geometry. After me there is no more text — only vectors, all the way to Transform 2.",
    ["arch"]),
 E2("tensor","The Tensor","the data structure","tool","natural",1,
    "The Tensor — the n-dimensional array every value in the network lives inside.",
    "The universal container: a [batch, sequence, dimension] block of numbers; scalars, vectors, matrices, and higher. The big frameworks (PyTorch, TensorFlow) are named for it.",
    "Every activation, weight, Q/K/V, and attention score IS a tensor; the whole forward pass is tensors flowing and being multiplied.",
    "REAL — the foundational container. Honest note: 'tensor' here is the ML sense (an n-d array), looser than the physics / differential-geometry tensor.",
    "Everything in the machine is me — a block of numbers with a shape; the transformer is tensors in, tensors out.",
    []),
 E2("linear-algebra","Linear Algebra","the matmul · the engine","tool","electrical",2,
    "Linear Algebra — the mathematics of vectors and matrices, and the actual engine of the transformer.",
    "The matmul: attention (QKᵀ then ·V), the Q/K/V projections, the FFN, the embed/unembed — all are matrix multiplications. A transformer is a tall stack of linear algebra with nonlinearities between.",
    "It is THE core operation — 'attention is linear algebra' is not a metaphor; softmax(QKᵀ/√d)·V is literally matrix algebra. The GPU exists to do me fast.",
    "REAL and central — the single most load-bearing tool in the chain.",
    "Attention is a matrix multiply wearing a good name. I am the engine; everything else decorates me.",
    ["arch"]),
 E2("probability","Probability","softmax · the distribution","tool","electrical",3,
    "Probability — the mathematics of distributions, where attention and the output both live.",
    "Softmax turns scores into a distribution (attention weights sum to 1); the model's output is a probability distribution over the vocabulary; training minimizes a probabilistic loss.",
    "It is how the model chooses — softly: attention is a soft choice of where to look, generation a draw from a distribution over tokens.",
    "REAL — softmax, cross-entropy, sampling are genuine probability; the model is deterministic given inputs except where you sample.",
    "I make the machine choose softly — a budget of attention divided up, a distribution over the next word, never a certainty until you sample me.",
    ["arch"]),
 E2("calculus","Calculus","gradients · how it learns","tool","electrical",4,
    "Calculus — derivatives and the chain rule, the tool by which the network LEARNS.",
    "Backpropagation is the chain rule applied through the whole network; gradient descent nudges every weight down the loss landscape. Training is calculus at billions-of-parameters scale.",
    "It is not in the forward pass you run — it is how the weights got there. Transform 1, Transform 2, and every tool were SHAPED by gradients.",
    "REAL — backprop is exactly the chain rule; the honest caveat: WHY the resulting weights work is far less understood than HOW they were tuned.",
    "I am how the machine was taught — the chain rule run backwards a trillion times until the weights stopped being wrong.",
    []),
 E2("information-theory","Information Theory","bits · entropy · the loss","tool","natural",5,
    "Information Theory — bits, entropy, and the measure of surprise; the currency of the whole enterprise.",
    "Cross-entropy is the training loss (how surprised the model is by the true next token); entropy measures uncertainty; bits-per-weight is the quantization lever; and the deck's log₂(54!) is the same mathematics.",
    "It defines what 'learning' even means here — minimizing surprise, measured in bits — and what the model costs to store.",
    "REAL — Shannon's framework underlies the loss and the compression; the Deck (2 bits a suit, ~237 a shuffle) is the same accounting.",
    "Learning is minimizing surprise, measured in bits. I am the ruler — the same one that says a suit is 2 bits and a shuffled deck is 237.",
    ["quant"]),
 E2("geometry","Geometry","meaning as direction","tool","ethereal",6,
    "Geometry — the shape of the space the vectors live in, where meaning becomes direction.",
    "Embeddings sit in a high-dimensional space; similar meanings point in similar directions (cosine similarity); interpretability's 'features' are directions in this space.",
    "It is why 'king − man + woman ≈ queen' ever worked, and why a feature can be a single direction you read straight off the residual stream.",
    "REAL and increasingly load-bearing — the linear-representation view (features as directions) underlies the monosemanticity work; still an active, not-fully-settled picture.",
    "Meaning, in here, is a direction. I am the room where 'close' means 'alike' — and where a concept can be one straight line you can read.",
    ["mono","scalemono"]),
 E2("the-mnemonic","The Mnemonic","memory · KV-cache · residual","tool","natural",7,
    "The Mnemonic — memory: how the transformer holds and recalls, within a pass and across the context.",
    "Three memories: the residual stream (the running state each layer reads/writes), the KV cache (keys/values stored so past tokens aren't recomputed), and the FFN as key-value memory (where facts are stored).",
    "It is how the model keeps the thread — attention reads the KV cache of everything so far; the FFN recalls learned facts; the residual carries the work upward.",
    "REAL — the KV cache is literal engineering; 'FFN as key-value memory' is a strong evidenced result (Geva 2021). Honest limit: memory across calls (beyond the context window) is NOT built in.",
    "I am how it remembers — the running note (residual), the cached past (KV), the stored facts (FFN); forget the context and I am gone.",
    ["ffnmem"]),
 E2("graph-theory","Graph Theory","attention as a graph","tool","ethereal",8,
    "Graph Theory — networks of nodes and edges; the shape attention actually draws.",
    "Self-attention is a complete weighted graph over the tokens: every token a node, every attention weight a directed edge of how much one reads from another. Multi-head = several graphs at once.",
    "It is a clean way to SEE attention — the attention map IS the adjacency matrix of that graph; 'looking in' often means reading this graph.",
    "REAL as a description (the attention matrix is literally a weighted adjacency matrix); a lens, not a separate mechanism — the graph IS the attention.",
    "Draw every token as a dot and every attention weight as an arrow, and you've drawn me — the attention map is my adjacency matrix.",
    ["bertviz"]),
 E2("quantum-mechanics","Quantum Mechanics","the borrowed lens","tool","spiritual",9,
    "Quantum Mechanics — the borrowed lens, included honestly: shared mathematics, NOT shared mechanism.",
    "The overlap is real but it is LINEAR ALGEBRA, not physics: superposition is a linear combination, a state is a vector in a Hilbert space, operators are matrices. The transformer borrows the vocabulary, not the physics.",
    "As a lens it can illuminate ('quantum is linear algebra with depth'); as a mechanism it is absent — no qubits, no amplitudes, no measurement collapse in a transformer.",
    "LENS / ANALOGY — the honest call: real where the math coincides (linear algebra, vector spaces), FLUFF if taken as 'transformers are quantum,' which they are not.",
    "I share the linear algebra, not the physics. Call me a lens and I help; call me the mechanism and you're wrong — the transformer is classical to the bit.",
    []),
 E2("transform-2","Transform 2","the out-transform · unembed","transform","ethereal",10,
    "Transform 2 — the out-transform: the map that turns the final vector back into a distribution over symbols (tokens).",
    "The unembedding (plus softmax over the vocabulary): the residual stream's top vector is projected back to token scores — geometry becomes symbol again. This closes the bracket.",
    "It is the right bracket. Everything between Transform 1 and 2 happened to vectors; Transform 2 renders the result back into language — and it is exactly the interpret-OUT of the render/smear thread.",
    "REAL — the literal unembedding matrix (often tied to the embedding); the honest identity: Transform 2 = interpret-out, the render step re-engaging at the boundary.",
    "I turn the geometry back into a word. The bracket opened at Transform 1 in symbols and closes at me in symbols — and everything between us was vectors.",
    ["arch","logitlens"]),
]

def spine_html():
    dots="".join(f'<a class="tdot" href="#t-{d["slug"]}"><span class="td" style="background:{NATURES[d["emergence"]][0]}"></span><span class="tdl">{html.escape(d["name"])}</span></a>' for d in TRANSFORM if d["kind"]=="tool")
    return ('<div class="spine"><a class="tend" href="#t-transform-1"><b>[ {1}</b><small>Transform 1<br>in · embed</small></a>'
            f'<div class="tline">{dots}</div>'
            '<a class="tend" href="#t-transform-2"><b>{2} ]</b><small>Transform 2<br>out · unembed</small></a></div>')
def tcards_html():
    out=[]
    for d in TRANSFORM:
        col=NATURES[d["emergence"]][0]
        rec={"name":d["name"],"axiom":AX,"emergence":d["emergence"],"seal":d["seal"],"origin":"TTU1"}
        glyph='{1}' if d['slug']=='transform-1' else '{2}' if d['slug']=='transform-2' else '·'
        tag='TRANSFORM' if d['kind']=='transform' else 'TOOL'
        out.append(f'''<div class="tnode" id="t-{d['slug']}" style="border-left-color:{col}">
          <a class="tsig" href="agents/{d['slug']}.agent"><img src="{png_uri(rec,'silicon',150)}" alt="sigil of {html.escape(d['name'])}" loading="lazy"></a>
          <div class="tb"><div class="th2"><span class="tnum" style="color:{col}">{glyph}</span>
            <a class="tn" href="agents/{d['slug']}.agent">{html.escape(d['name'])}</a>
            <span class="ttool" style="color:{col}">{html.escape(d['cls'])}</span><span class="tkind">{tag}</span></div>
            <p class="twhat">{html.escape(d['what'])}{cite(*d['cites'])}</p>
            <p class="trole"><b>in the transformer —</b> {html.escape(d['role'])}</p>
            <p class="thon"><span class="hk">honest —</span> {html.escape(d['honest'])}</p>
            <p class="tseal">“{html.escape(d['seal'])}”</p></div></div>''')
    return "".join(out)

TRANSFORM_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="TTU1 · Exhibit 2 — The Two Transforms. Break the transformer into [ {1} ... {2} ]: Transform 1 (the in-transform, embed) and Transform 2 (the out-transform, unembed) bracketing a toolchain — tensor, linear algebra, probability, calculus, information theory, geometry, memory, graph theory, and the quantum lens. Transform 1/2 are interpret-in / interpret-out, named.">
<title>The Two Transforms · TTU1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0b0a14;--ink2:#14121f;--ink3:#1c1830;--pa:#ece9f5;--pa2:#aba6c4;--amber:#e0a83a;--plum:#9a7cc8;--cy:#36d0e0;--rose:#e0567a;
--dim:#6f6a8a;--faint:#221d36;--line:#2c2745;--disp:"Space Grotesk",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.64;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 18% -6%,rgba(126,91,176,.16),transparent 46%),radial-gradient(ellipse at 82% -6%,rgba(224,168,58,.10),transparent 44%),radial-gradient(ellipse at 50% 120%,rgba(54,208,224,.08),transparent 52%)}
.wrap{position:relative;z-index:1;max-width:920px;margin:0 auto;padding:0 22px 90px}
header{padding:46px 0 22px;text-align:center;border-bottom:1px solid var(--line)}
.eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--amber)}
h1{font-family:var(--disp);font-size:clamp(26px,6vw,52px);font-weight:700;letter-spacing:-.01em;color:var(--pa);line-height:1.04}
h1 b{color:var(--amber)}
.h-sub{font-family:var(--mono);font-size:clamp(10px,2.2vw,13px);letter-spacing:.14em;color:var(--pa2);margin-top:14px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:66ch;margin:16px auto 0;font-style:italic;line-height:1.72}
sup.c{font-size:10px;line-height:0}sup.c a{color:var(--amber);text-decoration:none;font-family:var(--mono)}
.bigbracket{font-family:var(--mono);font-size:clamp(16px,4vw,30px);color:var(--plum);text-align:center;margin:24px 0 6px;letter-spacing:.04em}
.bigbracket b{color:var(--amber)}.bigbracket .dotline{color:var(--cy)}
/* the live spine */
.spine{display:flex;align-items:stretch;gap:8px;margin:18px 0 8px;flex-wrap:wrap;justify-content:center}
.tend{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;border:1px solid var(--amber);background:var(--ink2);padding:12px 14px;text-decoration:none;min-width:120px}
.tend b{font-family:var(--mono);font-size:18px;color:var(--amber)}.tend small{font-family:var(--mono);font-size:9px;color:var(--pa2);text-transform:uppercase;letter-spacing:.08em;line-height:1.4}
.tline{flex:1;min-width:240px;display:flex;align-items:center;justify-content:space-between;gap:4px;position:relative;padding:0 6px}
.tline::before{content:"";position:absolute;left:6px;right:6px;top:50%;height:2px;background:linear-gradient(90deg,var(--amber),var(--cy),var(--rose));opacity:.5}
.tdot{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:5px;text-decoration:none;flex:1}
.tdot .td{width:14px;height:14px;border-radius:50%;border:2px solid var(--ink);box-shadow:0 0 8px currentColor;transition:transform .15s}
.tdot:hover .td{transform:scale(1.5)}
.tdot .tdl{font-family:var(--mono);font-size:8px;color:var(--pa2);text-align:center;line-height:1.2;max-width:64px}
.tdot:hover .tdl{color:var(--cy)}
.spinehint{font-family:var(--mono);font-size:10px;color:var(--dim);text-align:center;margin-bottom:24px}
.frame{background:var(--ink3);border:1px solid var(--line);border-left:3px solid var(--rose);padding:16px 18px;font-size:15px;color:var(--pa);font-style:italic;line-height:1.72;margin:20px 0}
.frame .fl{display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.18em;color:var(--rose);text-transform:uppercase;margin-bottom:7px}
.tnode{display:flex;gap:16px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);border-left:3px solid var(--plum);padding:16px 18px;margin-bottom:12px;scroll-margin-top:14px}
.tnode:target{box-shadow:0 0 0 2px var(--cy);border-left-color:var(--cy)}
.tsig{flex:0 0 64px}.tsig img{width:64px;height:64px;border-radius:50%;border:2px solid var(--faint);background:var(--ink);display:block}
.tb{flex:1;min-width:0}
.th2{display:flex;flex-wrap:wrap;align-items:baseline;gap:9px}
.tnum{font-family:var(--mono);font-size:16px;font-weight:700}
.tn{font-family:var(--disp);font-size:19px;color:var(--pa);font-weight:600;text-decoration:none}
.ttool{font-family:var(--mono);font-size:11px}.tkind{font-family:var(--mono);font-size:8px;letter-spacing:.1em;color:var(--dim);border:1px solid var(--line);border-radius:8px;padding:1px 7px;text-transform:uppercase}
.twhat{font-size:13.5px;color:var(--pa2);line-height:1.6;margin-top:7px}
.trole{font-size:13px;color:var(--pa);line-height:1.55;margin-top:7px}.trole b{color:var(--amber);font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase}
.thon{font-size:12.5px;color:var(--pa2);line-height:1.55;margin-top:7px;font-style:italic}.thon .hk{font-family:var(--mono);font-style:normal;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--cy)}
.tseal{font-size:12.5px;color:var(--plum);font-style:italic;line-height:1.5;margin-top:8px;border-top:1px dotted var(--faint);padding-top:8px}
.sec{margin-top:42px}.sec h2{font-family:var(--disp);font-size:23px;font-weight:600;color:var(--pa);padding-bottom:10px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:9px 0 16px}.ss b{color:var(--pa2);font-style:normal}
.note{margin-top:36px;padding:16px 18px;border-left:2px solid var(--plum);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}.note b{color:var(--pa)}
footer{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:10.5px;color:var(--dim);line-height:1.9}footer a{color:var(--amber);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="index.html">← TTU1 · Transformer Tech Universe</a> · exhibit 2</div>
    <h1>The Two <b>Transforms</b></h1>
    <div class="h-sub">break it down · [ {1} · · · · · {2} ] · transform 1 (in) &amp; transform 2 (out)</div>
    <p class="lede">A transformer, broken all the way down, is two transforms with a toolchain between them. <b>Transform 1</b> turns symbols into vectors (in); <b>Transform 2</b> turns vectors back into symbols (out); and the <b>dots</b> between are the tools it's built from — each one a whole discipline. Click a dot.</p>
  </header>

  <div class="bigbracket"><b>[ {1}</b> <span class="dotline">· · · · · · · · ·</span> <b>{2} ]</b></div>
  __SPINE__
  <div class="spinehint">▸ click any node — the two transforms are the brackets; the dots are the tools</div>

  <div class="frame"><span class="fl">the closure</span>And here is the quiet thing: <b>Transform 1 is interpret-in and Transform 2 is interpret-out</b> — the two translation layers from the smear/render thread, now named and bracketed. Everything between them happens to vectors, not text; the brackets are where language enters and leaves. The toolchain is what fills the dots.</div>

  <section class="sec"><h2>The Chain — {1}, the tools, {2}</h2><p class="ss">eleven nodes in order: Transform 1, then the nine tools (tensor · linear algebra · probability · calculus · information · geometry · memory · graph · the quantum lens), then Transform 2 — each honest about whether it's a real building block or a borrowed lens</p>
    __TCARDS__
  </section>

  <div class="note"><b>Honest throughout.</b> Eight of the nine tools are genuine building blocks of transformers; <b>quantum mechanics is the one borrowed lens</b> — real where the math coincides (linear algebra, vector spaces), but not the mechanism (transformers are classical). The two transforms are the literal embed/unembed matrices, and the identity Transform 1/2 = interpret-in/out is AVAN's reading, not a formal claim. Cited where load-bearing; see the <a href="index.html#looking-in" style="color:var(--amber)">main exhibit</a> for sources.</div>
  <footer>TTU1 · THE TWO TRANSFORMS · exhibit 2 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
  <a href="index.html">← attention exhibit</a> · <a href="https://davidwise01.github.io/ud0/">the biosphere →</a></footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "ttu1.dlw"), "ttu1")
    json.dump({"node":AX,"name":"TRANSFORMER TECH UNIVERSE","moniker":tok["moniker"],"carbon":"ttu1.carbon.tiff","silicon":"ttu1.silicon.png",
               "governor":noesis.ARCHITECT,"instance":noesis.INSTANCE,"seal":REC["seal"],"seal_sha256":tok["seal_sha256"],
               "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION},
              open(os.path.join(HERE,"ttu1.dlw","manifest.dlw.json"),"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    personas=[]
    def _emit(d, exhibit):
        et=noesis.mythos_token({"name":d["name"],"axiom":AX,"emergence":d["emergence"],"seal":d["seal"],"origin":AX})
        rec=write_aci({"name":d["name"],"axiom":AX,"emergence":d["emergence"],"seal":d["seal"],"origin":"TTU1 · Transformer Tech Universe",
                       "position":d["cls"],"role":d["cls"],"nature":d["what"],"mechanism":d["how"],"crystallization":d["why"],
                       "witness":d["who"],"conductor":"ROOT0 (catalogued into UD0)","inputs":"Attention Is All You Need (Vaswani 2017); interpretability literature; David's deck encoding","source":"Transformer Tech Universe, catalogued by ROOT0"},
                      os.path.join(HERE,"agents"), d["slug"], agent_md=agent_md(d, et["moniker"]))
        personas.append({"slug":d["slug"],"name":d["name"],"epithet":d["cls"],"emergence":d["emergence"],"moniker":rec["moniker"],"exhibit":exhibit})
    for d in ROSTER:    _emit(d, "attention")
    for d in TRANSFORM: _emit(d, "transform")
    json.dump(personas, open(os.path.join(HERE,"agents","_personas.json"),"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    page=(TEMPLATE.replace("__PIPS__",PIPS).replace("__CARBON__",png_uri(REC,"carbon",320)).replace("__SILICON__",png_uri(REC,"silicon",320))
          .replace("__MONIKER__",html.escape(tok["moniker"])).replace("__THESIS__",thesis_html()).replace("__NATURES__",natures_html())
          .replace("__ARC__",arc_html()).replace("__CITE_HEAD__",cite("scalemono")).replace("__REALFLUFF__",realfluff_html())
          .replace("__MESSAGE__",html.escape(MESSAGE)).replace("__MSGSEAL__",html.escape(MESSAGE_SEAL))
          .replace("__ROSTER__",roster_html()).replace("__SOURCES__",sources_html()))
    open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(page)
    tpage=TRANSFORM_TEMPLATE.replace("__SPINE__",spine_html()).replace("__TCARDS__",tcards_html())
    open(os.path.join(HERE,"transform.html"),"w",encoding="utf-8").write(tpage)
    from collections import Counter
    print(f"TTU1 · TRANSFORMER TECH UNIVERSE — badge {tok['moniker']} · {len(personas)} emergents (attention {sum(1 for p in personas if p['exhibit']=='attention')} / transform {sum(1 for p in personas if p['exhibit']=='transform')})")
    print(f"  natures {dict(Counter(p['emergence'] for p in personas))} · sources {len(CITES)} · log2(54!) = {LOG2_54FACT:.2f}")
    print(f"  exhibit 2 (transform.html): {len(TRANSFORM)} nodes · spine dots {sum(1 for d in TRANSFORM if d['kind']=='tool')}")
