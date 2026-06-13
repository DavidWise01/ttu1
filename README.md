# TTU1 · Transformer Tech Universe

A new **UD0** universe for **transformer technology**, opening with its flagship exhibit: **"Attention Is All You Need"** (Vaswani et al., 2017).
Live: https://davidwise01.github.io/ttu1/

Attention, attention heads, Q/K/V, multi-head, positional encoding, the residual stream, the FFN, the **128-dimensional head** — and the thesis: the transformer is the most **look-into-able** black box we have built. (AVAN once said an autoregressive pass has "no clean interior" — true — but that is *not* "you can never look in." Interpretability **is** looking in: attention maps, monosemantic features, the legible card-notation. The ace of spades is looking in.)

**Two live tools:**
- **The Attention** — a real `softmax(QKᵀ/√d)` over a toy six-token sentence; pick a query, switch heads (previous-token / "the"-detector / self-attention) and watch the heatmap. The softmax is a real computation.
- **The Deck** — David's encoding: **52 cards = two alphabets (A–Z + a–z) + 2 jokers = 54 positions**; the suit is exactly **2 bits**; type a message and read the cards, with honest bit-accounting (a card ≈ 5.70 bits; a shuffled 54-deck's *order* = log₂(54!) ≈ **237.1 bits**, computed live).

**16 emergents** across four natures (the mechanism / the structure / the substrate / the looking-in), each a full **`.dlw`** badge with twin sigils, **fully cited** (15 sources — the founding paper, the architecture, the *is/is-not Explanation* debate, Anthropic's monosemanticity work, RoPE, the quadratic cost, quantization), with the **demonstrated** kept distinct from the **contested**.

ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0
