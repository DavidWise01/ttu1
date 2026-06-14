"use strict";

window.__rendererErrors = [];
window.addEventListener("error", (event) => {
  window.__rendererErrors.push(event.message || "renderer error");
});
window.addEventListener("unhandledrejection", (event) => {
  window.__rendererErrors.push(String(event.reason || "unhandled rejection"));
});

const $ = (id) => document.getElementById(id);
const canvas = $("mainCanvas");
const ctx = canvas.getContext("2d");
const TAU = Math.PI * 2;

const color = {
  bg: "#06070c",
  panel: "#111622",
  panel2: "#192031",
  line: "#293142",
  line2: "#3b465d",
  ink: "#eff3f7",
  muted: "#a8b0bd",
  faint: "#6f7a8c",
  cyan: "#3dd6c6",
  blue: "#54a7ff",
  amber: "#f2b84b",
  rose: "#f0718a",
  green: "#7bd88f",
  violet: "#b294ff"
};

const modules = [
  {
    id: "primer",
    number: "00",
    short: "Primer",
    title: "From text to the next token",
    kicker: "Transformer Inference - Instrument 00 - Primer",
    intro: "A transformer predicts one token at a time. Text becomes token IDs, IDs become vectors, vectors exchange context through attention, layers refine the residual stream, and a final projection turns the result into probabilities over the vocabulary.",
    concepts: ["token IDs", "embeddings", "attention", "residual stream", "logits", "backprop"],
    tabs: [{ id: "map", label: "Forward pass" }, { id: "loop", label: "Token loop" }, { id: "train", label: "Training view" }],
    note: "The same forward pass runs every time the model extends text. Training adds the reverse pass: measure error, send gradients backward, update weights, repeat.",
    reading: [
      ["One job", "Inference is repeated next-token prediction. The surprising part is how much context is compressed into the final vector."],
      ["Many tables", "Embedding tables, attention projections, MLP weights, and output projections are all learned matrices."],
      ["Same machine", "The model used at inference is the same model trained by backprop; only the gradient updates are absent."]
    ]
  },
  {
    id: "tokens",
    number: "01",
    short: "Tokens",
    title: "Turning words into vectors",
    kicker: "Transformer Inference - Instrument 01 - Tokens and Embeddings",
    intro: "Before the model can reason, language has to become numbers. Text is split into tokens, every token indexes a learned vector, and position information is added so the model can distinguish the same words in different orders.",
    concepts: ["byte-pair merges", "embedding matrix", "nearest neighbors", "analogies", "positional encoding"],
    tabs: [{ id: "bpe", label: "Tokenization" }, { id: "space", label: "Embedding space" }, { id: "analogy", label: "Geometry" }, { id: "position", label: "Position" }],
    note: "Tokens are not words. Common words often get one token; uncommon strings are built from smaller learned pieces.",
    reading: [
      ["Tokenizer", "A tokenizer is learned from text statistics. It compresses common chunks and keeps rare strings recoverable."],
      ["Embedding", "A token ID is just a row lookup in a learned matrix. The row is the token vector."],
      ["Position", "The model receives content plus location because order changes meaning."]
    ]
  },
  {
    id: "attention",
    number: "02",
    short: "Attention",
    title: "Letting every token read the room",
    kicker: "Transformer Inference - Instrument 02 - Attention",
    intro: "Attention gives each token a way to gather information from other tokens. Queries ask what is needed, keys advertise what each token has, values carry the content that gets mixed into the residual stream.",
    concepts: ["queries", "keys", "values", "score matrix", "causal mask", "multi-head attention"],
    tabs: [{ id: "qkv", label: "Q K V" }, { id: "scores", label: "Scores" }, { id: "mask", label: "Mask" }, { id: "heads", label: "Heads" }],
    note: "A causal language model can look left, including at the current token, but not into future tokens it has not generated yet.",
    reading: [
      ["Query", "The current token creates a query vector that searches for useful context."],
      ["Key", "Every token creates a key vector. Query dot key gives a compatibility score."],
      ["Value", "Attention weights mix value vectors into a new context vector."]
    ]
  },
  {
    id: "block",
    number: "03",
    short: "Block",
    title: "The transformer block repeats the work",
    kicker: "Transformer Inference - Instrument 03 - Transformer Block",
    intro: "A transformer block alternates attention with a small neural network, writing both results back into the residual stream. Normalization keeps the stream numerically stable as dozens of blocks compound their edits.",
    concepts: ["residual stream", "layer norm", "attention sublayer", "MLP", "GELU", "stack depth"],
    tabs: [{ id: "stream", label: "Residual" }, { id: "norm", label: "Normalize" }, { id: "mlp", label: "MLP" }, { id: "stack", label: "Stack" }],
    note: "The residual stream is the shared workspace. Each sublayer reads it, writes an update, and passes the edited stream onward.",
    reading: [
      ["Residual add", "Sublayers add changes instead of replacing the whole vector, which stabilizes deep stacks."],
      ["Layer norm", "Normalization makes the scale predictable before attention and MLP transformations."],
      ["MLP", "The feed-forward network expands dimensions, applies a nonlinearity, then projects back."]
    ]
  },
  {
    id: "logits",
    number: "04",
    short: "Logits",
    title: "From final vector to sampled token",
    kicker: "Transformer Inference - Instrument 04 - Logits and Sampling",
    intro: "The final vector is projected across the vocabulary to produce logits: raw scores for possible next tokens. Softmax turns scores into probabilities, and decoding settings decide how deterministic or adventurous the next pick will be.",
    concepts: ["unembedding", "logits", "softmax", "temperature", "top-k", "nucleus sampling"],
    tabs: [{ id: "projection", label: "Projection" }, { id: "softmax", label: "Softmax" }, { id: "decode", label: "Decode" }, { id: "stream", label: "Stream" }],
    note: "Lower temperature sharpens the distribution. Higher temperature spreads probability into alternatives.",
    reading: [
      ["Logits", "A logit is a raw compatibility score between the final state and a vocabulary token."],
      ["Softmax", "Softmax exponentiates and normalizes logits so all probabilities sum to one."],
      ["Sampling", "Greedy decoding picks the top token; sampling can preserve useful variety."]
    ]
  },
  {
    id: "training",
    number: "05",
    short: "Training",
    title: "The reverse pass that taught the model",
    kicker: "Transformer Inference - Instrument 05 - Training",
    intro: "During training, the model predicts the next token, compares that prediction to the true token, and uses backpropagation to compute how every weight contributed to the error. The optimizer turns those gradients into small weight updates.",
    concepts: ["cross entropy", "gradient", "backpropagation", "optimizer step", "batch", "learning rate"],
    tabs: [{ id: "loss", label: "Loss" }, { id: "backprop", label: "Backprop" }, { id: "opt", label: "Optimizer" }, { id: "batch", label: "Batches" }],
    note: "Inference runs the forward pass only. Training runs forward, loss, backward, optimizer, then repeats across huge batches of text.",
    reading: [
      ["Loss", "Cross entropy punishes confident wrong predictions more than uncertain wrong ones."],
      ["Gradient", "A gradient says how changing a weight would change the loss."],
      ["Optimizer", "Modern optimizers scale and smooth gradient updates instead of using raw gradients directly."]
    ]
  },
  {
    id: "representations",
    number: "06",
    short: "Reps",
    title: "Representations inside the residual stream",
    kicker: "Transformer Inference - Instrument 06 - Representations",
    intro: "Inside the model, features become directions and regions in activation space. Some directions track sentiment, syntax, entities, or style; later layers remix those features into the final decision.",
    concepts: ["activation space", "features", "linear probes", "steering vectors", "circuits", "layer evolution"],
    tabs: [{ id: "map", label: "Feature map" }, { id: "probe", label: "Probe" }, { id: "steer", label: "Steer" }, { id: "circuit", label: "Circuit" }],
    note: "Representations are not hand-authored rules. They are learned coordinates that become useful because they reduce prediction loss.",
    reading: [
      ["Feature", "A feature can act like a direction in activation space, not a single dedicated neuron."],
      ["Probe", "A simple classifier can reveal information already encoded in hidden states."],
      ["Steering", "Adding a direction can bias behavior, but it is an intervention, not a full explanation."]
    ]
  },
  {
    id: "fieldnotes",
    number: "07",
    short: "Notes",
    title: "Field notes from the model room",
    kicker: "Transformer Inference - Instrument 07 - Field Notes",
    intro: "This final instrument adds the practical lessons I would keep on a whiteboard: how to think about the model, what not to over-trust, what matters in production, and how to debug surprising outputs without getting lost.",
    concepts: ["mental model", "failure modes", "latency budget", "KV cache", "evals", "debug loop"],
    tabs: [{ id: "mental", label: "Mental model" }, { id: "traps", label: "Traps" }, { id: "production", label: "Production" }, { id: "debug", label: "Debug loop" }],
    note: "The useful posture is neither awe nor cynicism. Treat the model as a probabilistic system with a huge learned prior, a finite context window, and knobs that change behavior.",
    reading: [
      ["My favorite simplification", "The model is not recalling a single answer. It is compressing the prompt into a state that makes some continuations easier to believe than others."],
      ["The sharp edge", "Fluent text is not calibrated truth. The system can sound certain when its evidence path is thin, ambiguous, or missing."],
      ["The production lesson", "Most real quality comes from context, constraints, evals, retrieval, tool design, and feedback loops, not from prompt cleverness alone."]
    ]
  }
];

const defaults = {
  activeIndex: 0,
  tabs: {},
  done: [],
  primerStep: 0,
  bpeMerges: 0,
  bpeRun: false,
  selectedWord: "king",
  analogy: "royal",
  position: 5,
  attentionQuery: 2,
  attentionFocus: 1.2,
  causalMask: true,
  attentionHead: "local",
  blockLayer: 4,
  normStrength: 0.82,
  mlpGain: 1.1,
  temperature: 0.85,
  topK: 5,
  decoding: "topk",
  sampleCursor: 0,
  trainingStep: 24,
  trainingRun: false,
  learningRate: 0.06,
  batchSize: 4,
  repLayer: 9,
  probe: "sentiment",
  steering: 0.2,
  noteDepth: 3,
  noteScenario: "debug",
  latencyBudget: 180
};

let state = loadState();
let doneSet = new Set(state.done || []);
let lastTick = 0;
let lastBpeTick = 0;
let lastTrainingTick = 0;

function loadState() {
  try {
    const raw = localStorage.getItem("transformer-inference-studio");
    return raw ? { ...defaults, ...JSON.parse(raw) } : { ...defaults };
  } catch {
    return { ...defaults };
  }
}

function saveState() {
  state.done = [...doneSet];
  localStorage.setItem("transformer-inference-studio", JSON.stringify(state));
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function activeModule() {
  return modules[state.activeIndex] || modules[0];
}

function activeTab(module = activeModule()) {
  return state.tabs[module.id] || module.tabs[0].id;
}

function tabLabel(module, id) {
  return module.tabs.find((tab) => tab.id === id)?.label || module.tabs[0].label;
}

function render() {
  const module = activeModule();
  const tab = activeTab(module);

  $("moduleNumber").textContent = `Instrument ${module.number}`;
  $("topTitle").textContent = module.short;
  $("lessonKicker").textContent = module.kicker;
  $("lessonTitle").textContent = module.title;
  $("lessonIntro").textContent = module.intro;
  $("instrumentLabel").textContent = tabLabel(module, tab);
  $("instrumentStatus").textContent = `instrument ${module.number}`;
  $("lessonNote").textContent = module.note;
  $("doneButton").textContent = doneSet.has(module.id) ? "Done" : "Mark done";
  $("prevButton").disabled = state.activeIndex === 0;
  $("nextButton").disabled = state.activeIndex === modules.length - 1;

  renderProgress();
  renderModuleList();
  renderConcepts(module);
  renderTabs(module, tab);
  renderControls(module, tab);
  renderMetrics(module, tab);
  renderReading(module);
  saveState();
}

function renderProgress() {
  const count = doneSet.size;
  $("progressText").textContent = `${count} / ${modules.length}`;
  $("progressFill").style.width = `${Math.round((count / modules.length) * 100)}%`;
}

function renderModuleList() {
  $("moduleList").innerHTML = modules.map((module, index) => {
    const active = index === state.activeIndex ? " active" : "";
    const done = doneSet.has(module.id) ? "Done" : "";
    return `<button type="button" class="module-button${active}" data-index="${index}">
      <span class="module-num">${escapeHTML(module.number)}</span>
      <span><strong>${escapeHTML(module.short)}</strong><span>${escapeHTML(module.title)}</span></span>
      <span class="done-pill">${done}</span>
    </button>`;
  }).join("");
}

function renderConcepts(module) {
  $("conceptStrip").innerHTML = module.concepts.map((item) => `<span>${escapeHTML(item)}</span>`).join("");
}

function renderTabs(module, tab) {
  $("tabStrip").innerHTML = module.tabs.map((item) => {
    const active = item.id === tab ? " active" : "";
    return `<button type="button" class="${active}" data-tab="${escapeHTML(item.id)}">${escapeHTML(item.label)}</button>`;
  }).join("");
}

function renderControls(module, tab) {
  $("controlPanel").innerHTML = controlsFor(module.id, tab);
}

function renderMetrics(module, tab) {
  $("metricList").innerHTML = metricsFor(module.id, tab).map(([key, value, tone]) => {
    const cls = tone ? ` class="${tone}"` : "";
    return `<div class="metric-row"><span>${escapeHTML(key)}</span><strong${cls}>${escapeHTML(value)}</strong></div>`;
  }).join("");
}

function renderReading(module) {
  $("readingGrid").innerHTML = module.reading.map(([title, body]) => (
    `<article class="reading-card"><h3>${escapeHTML(title)}</h3><p>${escapeHTML(body)}</p></article>`
  )).join("");
}

function group(title, inner) {
  return `<div class="control-group"><div class="control-title"><span>${escapeHTML(title)}</span></div>${inner}</div>`;
}

function slider(bind, label, min, max, step, value, suffix = "") {
  return `<div class="control-group">
    <div class="control-title"><span>${escapeHTML(label)}</span><strong>${escapeHTML(formatNumber(value, suffix))}</strong></div>
    <input type="range" min="${min}" max="${max}" step="${step}" value="${value}" data-bind="${bind}">
  </div>`;
}

function segmented(bind, items, value) {
  return `<div class="segmented">${items.map(([label, val]) => {
    const active = String(val) === String(value) ? " active" : "";
    return `<button type="button" class="${active}" data-bind="${bind}" data-value="${escapeHTML(val)}">${escapeHTML(label)}</button>`;
  }).join("")}</div>`;
}

function buttons(items) {
  return `<div class="button-row">${items.map(([label, command, active]) => {
    const cls = active ? " active" : "";
    return `<button type="button" class="${cls}" data-command="${escapeHTML(command)}">${escapeHTML(label)}</button>`;
  }).join("")}</div>`;
}

function toggle(bind, label, value) {
  const checked = value ? " checked" : "";
  return `<label class="toggle-row"><input type="checkbox" data-bind="${bind}"${checked}>${escapeHTML(label)}</label>`;
}

function formatNumber(value, suffix = "") {
  if (Number.isInteger(value)) return `${value}${suffix}`;
  return `${Number(value).toFixed(2)}${suffix}`;
}

function controlsFor(id, tab) {
  if (id === "primer") {
    return slider("primerStep", "pipeline stage", 0, 6, 1, state.primerStep);
  }

  if (id === "tokens") {
    if (tab === "bpe") {
      return slider("bpeMerges", "merges applied", 0, 6, 1, state.bpeMerges) +
        group("merge controls", buttons([["Step", "bpe-step"], [state.bpeRun ? "Pause" : "Run", "bpe-run", state.bpeRun], ["Reset", "bpe-reset"]]));
    }
    if (tab === "space") {
      return group("token", segmented("selectedWord", [["king", "king"], ["queen", "queen"], ["cat", "cat"], ["paris", "paris"], ["tokyo", "tokyo"], ["river", "river"]], state.selectedWord));
    }
    if (tab === "analogy") {
      return group("analogy", segmented("analogy", [["royal", "royal"], ["capital", "capital"], ["country", "country"]], state.analogy));
    }
    return slider("position", "position", 0, 31, 1, state.position);
  }

  if (id === "attention") {
    const q = slider("attentionQuery", "query token", 0, ATTN_TOKENS.length - 1, 1, state.attentionQuery);
    const focus = slider("attentionFocus", "focus", 0.5, 2.2, 0.05, state.attentionFocus);
    const mask = group("visibility", toggle("causalMask", "causal mask", state.causalMask));
    const head = group("head pattern", segmented("attentionHead", [["local", "local"], ["syntax", "syntax"], ["entity", "entity"], ["recency", "recency"]], state.attentionHead));
    return tab === "heads" ? head + q : q + focus + mask;
  }

  if (id === "block") {
    return slider("blockLayer", "layer", 1, 12, 1, state.blockLayer) +
      slider("normStrength", "normalization", 0.4, 1.25, 0.05, state.normStrength) +
      slider("mlpGain", "MLP gain", 0.5, 1.8, 0.05, state.mlpGain);
  }

  if (id === "logits") {
    return slider("temperature", "temperature", 0.2, 2.0, 0.05, state.temperature) +
      slider("topK", "top-k", 1, 10, 1, state.topK) +
      group("decoding", segmented("decoding", [["greedy", "greedy"], ["top-k", "topk"], ["nucleus", "nucleus"]], state.decoding)) +
      group("sample", buttons([["Draw token", "sample"], ["Reset", "sample-reset"]]));
  }

  if (id === "training") {
    return slider("learningRate", "learning rate", 0.01, 0.18, 0.005, state.learningRate) +
      slider("batchSize", "batch size", 1, 8, 1, state.batchSize) +
      group("optimizer", buttons([["Step", "train-step"], [state.trainingRun ? "Pause" : "Run", "train-run", state.trainingRun], ["Reset", "train-reset"]]));
  }

  if (id === "representations") {
    return slider("repLayer", "layer", 1, 16, 1, state.repLayer) +
      slider("steering", "steering", -1.5, 1.5, 0.05, state.steering) +
      group("probe", segmented("probe", [["sentiment", "sentiment"], ["entity", "entity"], ["syntax", "syntax"], ["style", "style"]], state.probe));
  }

  if (id === "fieldnotes") {
    const base = slider("noteDepth", "detail", 1, 5, 1, state.noteDepth) +
      group("scenario", segmented("noteScenario", [["debug", "debug"], ["ship", "ship"], ["teach", "teach"], ["eval", "eval"]], state.noteScenario));
    return tab === "production" ? base + slider("latencyBudget", "token budget ms", 60, 420, 10, state.latencyBudget, " ms") : base;
  }

  return "";
}

function metricsFor(id, tab) {
  if (id === "primer") {
    const stage = PIPELINE[state.primerStep];
    return [["stage", stage.label, "cool"], ["tokens", "6"], ["vector width", "12 dims"], ["loop", "one token at a time"]];
  }

  if (id === "tokens") {
    if (tab === "bpe") {
      const st = BPE.states[state.bpeMerges];
      const total = Object.keys(CORPUS).reduce((sum, word) => sum + st[word].length * CORPUS[word], 0);
      return [["merges", `${state.bpeMerges} / 6`, "cool"], ["corpus tokens", total], ["unseen word", applyBPE("lowest", state.bpeMerges).join(" ")]];
    }
    if (tab === "space") {
      const neighbors = nearestWords(state.selectedWord, 3).map(([w]) => w).join(", ");
      return [["token", state.selectedWord, "cool"], ["nearest", neighbors], ["matrix row", `E[${wordIndex(state.selectedWord)}]`]];
    }
    if (tab === "analogy") {
      const result = analogyResult(state.analogy);
      return [["expression", result.expr], ["nearest", result.best, "good"], ["distance", result.distance.toFixed(2)]];
    }
    return [["position", state.position], ["dims", "16"], ["neighbor sim", cosine(PE(state.position), PE((state.position + 1) % 32)).toFixed(3), "cool"]];
  }

  if (id === "attention") {
    const data = attentionData();
    return [["query", ATTN_TOKENS[state.attentionQuery].t, "cool"], ["top key", data.topToken, "good"], ["entropy", entropy(data.probs).toFixed(2)], ["mask", state.causalMask ? "on" : "off"]];
  }

  if (id === "block") {
    return [["layer", `${state.blockLayer} / 12`, "cool"], ["stream", "residual"], ["norm scale", state.normStrength.toFixed(2)], ["MLP gain", state.mlpGain.toFixed(2)]];
  }

  if (id === "logits") {
    const probs = decodedProbs();
    const best = topIndex(probs);
    return [["mode", state.decoding], ["selected", VOCAB[pickIndex(probs)].word, "good"], ["top prob", `${Math.round(probs[best] * 100)}%`, "cool"], ["entropy", entropy(probs).toFixed(2)]];
  }

  if (id === "training") {
    return [["step", state.trainingStep], ["loss", lossAt(state.trainingStep).toFixed(3), "cool"], ["grad norm", gradNorm(state.trainingStep).toFixed(3)], ["batch", `${state.batchSize} sequences`]];
  }

  if (id === "representations") {
    return [["layer", state.repLayer, "cool"], ["probe", state.probe], ["steering", state.steering.toFixed(2)], ["confidence", `${Math.round(probeScore() * 100)}%`, "good"]];
  }

  if (id === "fieldnotes") {
    const scores = fieldNoteScores();
    return [["scenario", state.noteScenario, "cool"], ["detail", `${state.noteDepth} / 5`], ["risk focus", scores.topRisk, "warn"], ["ship lever", scores.shipLever, "good"]];
  }

  return [];
}

$("moduleList").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-index]");
  if (!button) return;
  state.activeIndex = Number(button.dataset.index);
  render();
});

$("tabStrip").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-tab]");
  if (!button) return;
  state.tabs[activeModule().id] = button.dataset.tab;
  render();
});

$("controlPanel").addEventListener("input", (event) => {
  const input = event.target.closest("[data-bind]");
  if (!input) return;
  const key = input.dataset.bind;
  state[key] = input.type === "checkbox" ? input.checked : Number(input.value);
  render();
});

$("controlPanel").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;

  if (button.dataset.bind) {
    const key = button.dataset.bind;
    const raw = button.dataset.value;
    state[key] = isFinite(Number(raw)) && raw.trim() !== "" ? Number(raw) : raw;
    render();
    return;
  }

  runCommand(button.dataset.command);
});

$("prevButton").addEventListener("click", () => {
  state.activeIndex = Math.max(0, state.activeIndex - 1);
  render();
});

$("nextButton").addEventListener("click", () => {
  state.activeIndex = Math.min(modules.length - 1, state.activeIndex + 1);
  render();
});

$("doneButton").addEventListener("click", () => {
  const id = activeModule().id;
  if (doneSet.has(id)) doneSet.delete(id);
  else doneSet.add(id);
  render();
});

function runCommand(command) {
  if (command === "bpe-step") state.bpeMerges = Math.min(6, state.bpeMerges + 1);
  if (command === "bpe-run") state.bpeRun = !state.bpeRun;
  if (command === "bpe-reset") {
    state.bpeMerges = 0;
    state.bpeRun = false;
  }
  if (command === "sample") state.sampleCursor += 1;
  if (command === "sample-reset") state.sampleCursor = 0;
  if (command === "train-step") state.trainingStep = Math.min(160, state.trainingStep + 1);
  if (command === "train-run") state.trainingRun = !state.trainingRun;
  if (command === "train-reset") {
    state.trainingStep = 0;
    state.trainingRun = false;
  }
  render();
}

function animationLoop(now) {
  const t = now / 1000;
  if (!lastTick) lastTick = now;

  if (state.bpeRun && now - lastBpeTick > 600) {
    lastBpeTick = now;
    state.bpeMerges += 1;
    if (state.bpeMerges >= 6) {
      state.bpeMerges = 6;
      state.bpeRun = false;
    }
    render();
  }

  if (state.trainingRun && now - lastTrainingTick > 160) {
    lastTrainingTick = now;
    state.trainingStep = Math.min(160, state.trainingStep + 1);
    if (state.trainingStep >= 160) state.trainingRun = false;
    render();
  }

  draw(t);
  requestAnimationFrame(animationLoop);
}

function fitCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(1, Math.floor(rect.width * dpr));
  const height = Math.max(1, Math.floor(rect.height * dpr));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { w: rect.width, h: rect.height };
}

function draw(t) {
  const { w, h } = fitCanvas();
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = color.bg;
  ctx.fillRect(0, 0, w, h);
  drawGrid(ctx, w, h);
  const module = activeModule();
  const tab = activeTab(module);
  if (module.id === "primer") drawPrimer(ctx, w, h, tab, t);
  if (module.id === "tokens") drawTokens(ctx, w, h, tab, t);
  if (module.id === "attention") drawAttention(ctx, w, h, tab, t);
  if (module.id === "block") drawBlock(ctx, w, h, tab, t);
  if (module.id === "logits") drawLogits(ctx, w, h, tab, t);
  if (module.id === "training") drawTraining(ctx, w, h, tab, t);
  if (module.id === "representations") drawRepresentations(ctx, w, h, tab, t);
  if (module.id === "fieldnotes") drawFieldNotes(ctx, w, h, tab, t);
}

function drawGrid(g, w, h) {
  g.save();
  g.strokeStyle = "rgba(41, 49, 66, 0.34)";
  g.lineWidth = 1;
  for (let x = 0; x < w; x += 36) {
    g.beginPath();
    g.moveTo(x, 0);
    g.lineTo(x, h);
    g.stroke();
  }
  for (let y = 0; y < h; y += 36) {
    g.beginPath();
    g.moveTo(0, y);
    g.lineTo(w, y);
    g.stroke();
  }
  g.restore();
}

function rgba(hex, alpha) {
  const value = parseInt(hex.slice(1), 16);
  return `rgba(${(value >> 16) & 255}, ${(value >> 8) & 255}, ${value & 255}, ${alpha})`;
}

function rect(g, x, y, w, h, r = 8, fill = color.panel, stroke = color.line) {
  g.beginPath();
  g.roundRect(x, y, w, h, r);
  g.fillStyle = fill;
  g.fill();
  if (stroke) {
    g.strokeStyle = stroke;
    g.lineWidth = 1;
    g.stroke();
  }
}

function label(g, text, x, y, size = 12, fill = color.muted, align = "left", weight = "400") {
  g.font = `${weight} ${size}px Consolas, "Courier New", monospace`;
  g.fillStyle = fill;
  g.textAlign = align;
  g.textBaseline = "middle";
  g.fillText(text, x, y);
}

function title(g, text, x, y, size = 18, fill = color.ink, align = "left") {
  g.font = `600 ${size}px "Segoe UI", system-ui, sans-serif`;
  g.fillStyle = fill;
  g.textAlign = align;
  g.textBaseline = "middle";
  g.fillText(text, x, y);
}

function wrapText(g, text, x, y, maxWidth, lineHeight, maxLines = 5) {
  const words = text.split(" ");
  let line = "";
  let row = 0;
  g.textAlign = "left";
  g.textBaseline = "top";
  for (const word of words) {
    const test = line ? `${line} ${word}` : word;
    if (g.measureText(test).width > maxWidth && line) {
      g.fillText(line, x, y + row * lineHeight);
      line = word;
      row += 1;
      if (row >= maxLines) return;
    } else {
      line = test;
    }
  }
  if (line && row < maxLines) g.fillText(line, x, y + row * lineHeight);
}

function heat(g, x, y, w, h, values, maxAbs) {
  const max = maxAbs || Math.max(0.01, ...values.map((v) => Math.abs(v)));
  const cw = w / values.length;
  values.forEach((value, i) => {
    const scaled = value / max;
    const c = scaled >= 0 ? color.cyan : color.rose;
    rect(g, x + i * cw + 0.5, y, Math.max(1, cw - 1), h, 2, rgba(c, 0.16 + 0.72 * Math.min(1, Math.abs(scaled))), null);
  });
  g.strokeStyle = color.line;
  g.strokeRect(x, y, w, h);
}

function arrow(g, x1, y1, x2, y2, c = color.cyan, width = 2, alpha = 1) {
  g.save();
  g.strokeStyle = rgba(c, alpha);
  g.fillStyle = rgba(c, alpha);
  g.lineWidth = width;
  g.beginPath();
  g.moveTo(x1, y1);
  g.lineTo(x2, y2);
  g.stroke();
  const a = Math.atan2(y2 - y1, x2 - x1);
  g.beginPath();
  g.moveTo(x2, y2);
  g.lineTo(x2 - 9 * Math.cos(a - 0.42), y2 - 9 * Math.sin(a - 0.42));
  g.lineTo(x2 - 9 * Math.cos(a + 0.42), y2 - 9 * Math.sin(a + 0.42));
  g.closePath();
  g.fill();
  g.restore();
}

function softmax(scores, temp = 1) {
  const max = Math.max(...scores);
  const exp = scores.map((score) => Math.exp((score - max) / temp));
  const total = exp.reduce((sum, value) => sum + value, 0);
  return exp.map((value) => value / total);
}

function topIndex(values) {
  let best = 0;
  for (let i = 1; i < values.length; i += 1) if (values[i] > values[best]) best = i;
  return best;
}

function entropy(probs) {
  return probs.reduce((sum, p) => sum + (p > 0 ? -p * Math.log2(p) : 0), 0);
}

function dist(a, b) {
  return Math.hypot(a[0] - b[0], a[1] - b[1]);
}

function cosine(a, b) {
  let d = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i += 1) {
    d += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return d / (Math.sqrt(na) * Math.sqrt(nb));
}

const PIPELINE = [
  { label: "tokens", detail: "Text is split into vocabulary pieces and converted to integer IDs.", c: color.cyan },
  { label: "embeddings", detail: "Each ID looks up a learned vector; position is added to preserve order.", c: color.green },
  { label: "attention", detail: "Queries compare to keys, weights mix values, and context joins the stream.", c: color.blue },
  { label: "blocks", detail: "Attention and MLP updates accumulate through repeated residual blocks.", c: color.violet },
  { label: "logits", detail: "The final vector scores every possible next token in the vocabulary.", c: color.amber },
  { label: "sample", detail: "Softmax and decoding settings select one token, then the loop runs again.", c: color.rose },
  { label: "learn", detail: "During training, gradients flow backward to improve the weights.", c: color.cyan }
];

function drawPrimer(g, w, h, tab, t) {
  const step = state.primerStep;
  const pad = 26;
  const cols = w > 760 ? 7 : 4;
  const boxW = (w - pad * 2 - (cols - 1) * 12) / cols;
  const boxH = 72;
  const startY = 54;

  PIPELINE.forEach((stage, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = pad + col * (boxW + 12);
    const y = startY + row * 104;
    const active = i === step;
    rect(g, x, y, boxW, boxH, 8, active ? rgba(stage.c, 0.14) : color.panel, active ? stage.c : color.line);
    label(g, String(i).padStart(2, "0"), x + 14, y + 20, 11, active ? stage.c : color.faint);
    title(g, stage.label, x + 14, y + 43, 15, active ? stage.c : color.ink);
    if (i < PIPELINE.length - 1 && col < cols - 1) {
      arrow(g, x + boxW + 2, y + boxH / 2, x + boxW + 10, y + boxH / 2, color.line2, 1, 0.8);
    }
  });

  const detailY = h * 0.49;
  rect(g, pad, detailY, w - pad * 2, h - detailY - pad, 8, "#0b0e15", color.line);
  const stage = PIPELINE[step];
  title(g, stage.label.toUpperCase(), pad + 22, detailY + 30, 18, stage.c);
  g.font = "14px Segoe UI, system-ui, sans-serif";
  g.fillStyle = color.muted;
  wrapText(g, stage.detail, pad + 22, detailY + 54, Math.min(470, w - pad * 2 - 44), 22, 3);

  if (tab === "map") drawPrimerMap(g, w, h, detailY, stage, t);
  if (tab === "loop") drawPrimerLoop(g, w, h, detailY, t);
  if (tab === "train") drawPrimerTrain(g, w, h, detailY, t);
}

function drawPrimerMap(g, w, h, detailY, stage, t) {
  const x = Math.max(w * 0.56, 430);
  const y = detailY + 38;
  const values = Array.from({ length: 12 }, (_, i) => Math.sin(i * 0.95 + t * 1.4 + state.primerStep));
  label(g, "activation vector", x, y - 12, 11, color.faint);
  heat(g, x, y, w - x - 42, 34, values);
  const barY = y + 72;
  const probs = softmax([2.3, 1.8, 0.7, 0.1, -0.5, 1.1], 0.9);
  drawBars(g, ["mat", "rug", "floor", "cat", "sky", "room"], probs, x, barY, w - x - 42, 120, stage.c, true);
}

function drawPrimerLoop(g, w, h, detailY, t) {
  const words = ["The", "model", "predicts", "one", "token", "at", "a", "time"];
  const visible = 1 + Math.floor((t * 1.3) % words.length);
  let x = Math.max(380, w * 0.48);
  const y = detailY + 52;
  words.forEach((word, i) => {
    const tw = 42 + word.length * 8;
    rect(g, x, y, tw, 34, 6, i < visible ? rgba(color.cyan, 0.14) : color.panel, i < visible ? color.cyan : color.line);
    label(g, word, x + tw / 2, y + 17, 12, i < visible ? color.cyan : color.faint, "center");
    x += tw + 8;
    if (x > w - 110) {
      x = Math.max(380, w * 0.48);
    }
  });
  label(g, "append selected token, rerun forward pass", Math.max(380, w * 0.48), detailY + 130, 12, color.muted);
}

function drawPrimerTrain(g, w, h, detailY, t) {
  const x = Math.max(390, w * 0.5);
  const y = detailY + 40;
  const lw = w - x - 46;
  const lh = 150;
  g.strokeStyle = color.line2;
  g.beginPath();
  g.moveTo(x, y);
  g.lineTo(x, y + lh);
  g.lineTo(x + lw, y + lh);
  g.stroke();
  g.strokeStyle = color.cyan;
  g.lineWidth = 2;
  g.beginPath();
  for (let i = 0; i <= 80; i += 1) {
    const px = x + (i / 80) * lw;
    const loss = 2.8 * Math.exp(-i / 26) + 0.18 + 0.04 * Math.sin(i * 0.4);
    const py = y + lh - (1 - Math.min(1, loss / 3)) * lh;
    if (i === 0) g.moveTo(px, py);
    else g.lineTo(px, py);
  }
  g.stroke();
  const p = (t * 18) % 80;
  const px = x + (p / 80) * lw;
  const loss = 2.8 * Math.exp(-p / 26) + 0.18;
  const py = y + lh - (1 - Math.min(1, loss / 3)) * lh;
  g.fillStyle = color.cyan;
  g.beginPath();
  g.arc(px, py, 5, 0, TAU);
  g.fill();
  label(g, "loss", x + 4, y + 12, 11, color.faint);
  label(g, "training steps", x + lw - 96, y + lh + 16, 11, color.faint);
}

const CORPUS = { low: 5, lower: 2, newest: 6, widest: 3 };
const BPE = makeBPE(CORPUS, 6);

function makeBPE(corpus, maxMerges) {
  const words = {};
  Object.keys(corpus).forEach((word) => {
    words[word] = [...word.split(""), "_"];
  });
  const clone = () => Object.fromEntries(Object.entries(words).map(([k, v]) => [k, [...v]]));
  const states = [clone()];
  const merges = [];
  for (let m = 0; m < maxMerges; m += 1) {
    const pairs = {};
    Object.entries(corpus).forEach(([word, count]) => {
      const symbols = words[word];
      for (let i = 0; i < symbols.length - 1; i += 1) {
        const key = `${symbols[i]}::${symbols[i + 1]}`;
        pairs[key] = (pairs[key] || 0) + count;
      }
    });
    const best = Object.entries(pairs).sort((a, b) => b[1] - a[1])[0];
    if (!best) break;
    const [left, right] = best[0].split("::");
    merges.push({ left, right, count: best[1] });
    Object.keys(words).forEach((word) => {
      const symbols = words[word];
      const next = [];
      for (let i = 0; i < symbols.length; i += 1) {
        if (i < symbols.length - 1 && symbols[i] === left && symbols[i + 1] === right) {
          next.push(left + right);
          i += 1;
        } else {
          next.push(symbols[i]);
        }
      }
      words[word] = next;
    });
    states.push(clone());
  }
  return { states, merges };
}

function applyBPE(word, count) {
  let symbols = [...word.split(""), "_"];
  BPE.merges.slice(0, count).forEach(({ left, right }) => {
    const next = [];
    for (let i = 0; i < symbols.length; i += 1) {
      if (i < symbols.length - 1 && symbols[i] === left && symbols[i + 1] === right) {
        next.push(left + right);
        i += 1;
      } else {
        next.push(symbols[i]);
      }
    }
    symbols = next;
  });
  return symbols.map((s) => s.replaceAll("_", "."));
}

const WMAP = {
  man: [2, 2], woman: [2, 4], king: [5, 2], queen: [5, 4], prince: [5, 2.7], princess: [5, 3.4],
  cat: [2, 7], dog: [3, 7.2], kitten: [2.1, 8], puppy: [3.1, 8],
  france: [8.2, 2], paris: [8.2, 4], italy: [10.3, 2], rome: [10.3, 4], japan: [12.4, 2], tokyo: [12.4, 4],
  river: [7, 7.6], bank: [7.8, 7.2], money: [8.8, 6.6]
};

const WCOL = {
  man: color.blue, king: color.blue, prince: color.blue,
  woman: color.rose, queen: color.rose, princess: color.rose,
  cat: color.amber, dog: color.amber, kitten: color.amber, puppy: color.amber,
  france: color.green, italy: color.green, japan: color.green,
  paris: color.cyan, rome: color.cyan, tokyo: color.cyan,
  river: color.violet, bank: color.violet, money: color.green
};

function wordIndex(word) {
  return Object.keys(WMAP).indexOf(word) + 1000;
}

function nearestWords(word, n) {
  return Object.keys(WMAP)
    .filter((key) => key !== word)
    .map((key) => [key, dist(WMAP[word], WMAP[key])])
    .sort((a, b) => a[1] - b[1])
    .slice(0, n);
}

function mapTransform(w, h) {
  const points = Object.values(WMAP);
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  const x0 = Math.min(...xs) - 1;
  const x1 = Math.max(...xs) + 1;
  const y0 = Math.min(...ys) - 1;
  const y1 = Math.max(...ys) + 1;
  const pad = 44;
  return {
    mx: (p) => pad + ((p[0] - x0) / (x1 - x0)) * (w - pad * 2),
    my: (p) => h - pad - ((p[1] - y0) / (y1 - y0)) * (h - pad * 2)
  };
}

function analogyResult(kind) {
  const config = {
    royal: ["king", "man", "woman", "king - man + woman"],
    capital: ["paris", "france", "italy", "paris - france + italy"],
    country: ["tokyo", "japan", "france", "tokyo - japan + france"]
  }[kind];
  const [a, b, c, expr] = config;
  const target = [WMAP[a][0] - WMAP[b][0] + WMAP[c][0], WMAP[a][1] - WMAP[b][1] + WMAP[c][1]];
  let best = "";
  let distance = Infinity;
  Object.keys(WMAP).forEach((word) => {
    if ([a, b, c].includes(word)) return;
    const d = dist(target, WMAP[word]);
    if (d < distance) {
      best = word;
      distance = d;
    }
  });
  return { a, b, c, expr, target, best, distance };
}

function PE(pos) {
  const dims = 16;
  return Array.from({ length: dims }, (_, i) => {
    const k = Math.floor(i / 2);
    const denom = Math.pow(10000, (2 * k) / dims);
    return i % 2 === 0 ? Math.sin(pos / denom) : Math.cos(pos / denom);
  });
}

function drawTokens(g, w, h, tab, t) {
  if (tab === "bpe") drawBPE(g, w, h);
  if (tab === "space") drawEmbeddingSpace(g, w, h);
  if (tab === "analogy") drawAnalogy(g, w, h, t);
  if (tab === "position") drawPosition(g, w, h);
}

function drawBPE(g, w, h) {
  const m = state.bpeMerges;
  const symbols = BPE.states[m];
  const pad = 28;
  title(g, "Byte-pair merges", pad, 34, 18, color.ink);
  let y = 72;
  Object.keys(CORPUS).forEach((word) => {
    label(g, `x${CORPUS[word]}`, pad, y + 16, 12, color.faint);
    let x = pad + 52;
    symbols[word].forEach((symbol) => {
      const display = symbol.replaceAll("_", ".");
      const tw = Math.max(34, display.length * 9 + 18);
      rect(g, x, y, tw, 32, 6, rgba(color.cyan, 0.08), color.line2);
      label(g, display, x + tw / 2, y + 16, 12, color.cyan, "center");
      x += tw + 7;
    });
    y += 48;
  });
  title(g, "Learned merge table", pad, y + 20, 15, color.muted);
  BPE.merges.slice(0, m).forEach((merge, i) => {
    const text = `${i + 1}. ${merge.left.replaceAll("_", ".")} + ${merge.right.replaceAll("_", ".")}  x${merge.count}`;
    label(g, text, pad, y + 48 + i * 21, 12, i === m - 1 ? color.amber : color.faint);
  });
  const unseen = applyBPE("lowest", m);
  let ux = Math.max(w * 0.58, 360);
  const uy = h - 84;
  title(g, "Unseen word: lowest", ux, uy - 24, 15, color.ink);
  unseen.forEach((symbol) => {
    const tw = Math.max(34, symbol.length * 9 + 18);
    rect(g, ux, uy, tw, 34, 6, rgba(color.violet, 0.12), color.violet);
    label(g, symbol, ux + tw / 2, uy + 17, 12, color.violet, "center");
    ux += tw + 8;
  });
}

function drawEmbeddingSpace(g, w, h) {
  const { mx, my } = mapTransform(w, h);
  const selected = state.selectedWord;
  const neighbors = new Set(nearestWords(selected, 3).map(([word]) => word));
  nearestWords(selected, 3).forEach(([word]) => {
    g.strokeStyle = rgba(color.cyan, 0.34);
    g.lineWidth = 1.5;
    g.beginPath();
    g.moveTo(mx(WMAP[selected]), my(WMAP[selected]));
    g.lineTo(mx(WMAP[word]), my(WMAP[word]));
    g.stroke();
  });
  Object.keys(WMAP).forEach((word) => {
    const p = WMAP[word];
    const active = word === selected;
    const near = neighbors.has(word);
    g.fillStyle = active ? color.cyan : rgba(WCOL[word] || color.muted, near ? 0.92 : 0.55);
    g.beginPath();
    g.arc(mx(p), my(p), active ? 7 : near ? 5 : 3.5, 0, TAU);
    g.fill();
    label(g, word, mx(p), my(p) - 13, active ? 12 : 10, active ? color.cyan : color.muted, "center", active ? "700" : "400");
  });
  const vec = Array.from({ length: 14 }, (_, i) => Math.sin(WMAP[selected][0] * 0.6 + i * 0.72) + Math.cos(WMAP[selected][1] * 0.7 - i * 0.4));
  label(g, `${selected} embedding row`, 28, h - 34, 12, color.faint);
  heat(g, 188, h - 46, w - 218, 24, vec);
}

function drawAnalogy(g, w, h, t) {
  const { mx, my } = mapTransform(w, h);
  const result = analogyResult(state.analogy);
  const involved = new Set([result.a, result.b, result.c, result.best]);
  Object.keys(WMAP).forEach((word) => {
    const p = WMAP[word];
    const active = involved.has(word);
    g.fillStyle = active ? WCOL[word] || color.ink : rgba(color.faint, 0.42);
    g.beginPath();
    g.arc(mx(p), my(p), active ? 5.5 : 2.6, 0, TAU);
    g.fill();
    if (active) label(g, word, mx(p), my(p) - 13, 11, WCOL[word] || color.ink, "center");
  });
  const pulse = Math.min(1, (t * 0.42) % 1.4);
  const drawVector = (from, to, c) => {
    const x1 = mx(from);
    const y1 = my(from);
    const x2 = x1 + (mx(to) - x1) * pulse;
    const y2 = y1 + (my(to) - y1) * pulse;
    arrow(g, x1, y1, x2, y2, c, 2.2, 0.94);
  };
  drawVector(WMAP[result.b], WMAP[result.a], color.violet);
  drawVector(WMAP[result.c], result.target, color.cyan);
  if (pulse >= 1) {
    g.strokeStyle = color.cyan;
    g.lineWidth = 2;
    g.beginPath();
    g.arc(mx(result.target), my(result.target), 12, 0, TAU);
    g.stroke();
  }
  title(g, `${result.expr} = ${result.best}`, 28, h - 30, 18, color.cyan);
}

function drawPosition(g, w, h) {
  const pad = 32;
  const rows = 32;
  const dims = 16;
  const hmW = Math.min(w * 0.58, 560);
  const hmH = h - 100;
  const cellW = hmW / dims;
  const cellH = hmH / rows;
  for (let row = 0; row < rows; row += 1) {
    const vec = PE(row);
    for (let col = 0; col < dims; col += 1) {
      const v = vec[col];
      const c = v >= 0 ? color.cyan : color.rose;
      g.fillStyle = rgba(c, 0.12 + Math.abs(v) * 0.75);
      g.fillRect(pad + col * cellW, 42 + row * cellH, cellW + 0.5, cellH + 0.5);
    }
  }
  g.strokeStyle = color.ink;
  g.strokeRect(pad - 1, 42 + state.position * cellH - 1, hmW + 2, cellH + 2);
  label(g, "position", pad, 26, 12, color.faint);
  label(g, "dimensions", pad + hmW / 2, h - 28, 12, color.faint, "center");
  const rightX = pad + hmW + 36;
  title(g, `Position ${state.position}`, rightX, 58, 18, color.ink);
  heat(g, rightX, 88, w - rightX - 28, 28, PE(state.position), 1);
  const baseY = 154;
  const graphH = 180;
  g.strokeStyle = color.line2;
  g.beginPath();
  g.moveTo(rightX, baseY + graphH);
  g.lineTo(w - 28, baseY + graphH);
  g.stroke();
  g.strokeStyle = color.cyan;
  g.lineWidth = 2;
  g.beginPath();
  for (let p = 0; p < rows; p += 1) {
    const sim = cosine(PE(state.position), PE(p));
    const x = rightX + (p / (rows - 1)) * (w - rightX - 28);
    const y = baseY + graphH - ((sim + 0.2) / 1.2) * graphH;
    if (p === 0) g.moveTo(x, y);
    else g.lineTo(x, y);
  }
  g.stroke();
  label(g, "similarity to other positions", rightX, baseY - 16, 12, color.faint);
}

const ATTN_TOKENS = [
  { t: "The", f: [0.1, 0.1, 0.1] },
  { t: "river", f: [1, 0.1, 0.9] },
  { t: "bank", f: [0.9, 0.25, 0.75] },
  { t: "turned", f: [0.15, 0.9, 0.35] },
  { t: "quiet", f: [0.1, 0.8, 0.25] },
  { t: "after", f: [0.3, 0.4, 0.5] },
  { t: "rain", f: [0.8, 0.15, 1] }
];

function attentionData(query = state.attentionQuery) {
  const scores = ATTN_TOKENS.map((token, i) => {
    const q = ATTN_TOKENS[query].f;
    const dot = q.reduce((sum, v, k) => sum + v * token.f[k], 0);
    const local = -Math.abs(query - i) * 0.16;
    const self = i === query ? 0.28 : 0;
    const masked = state.causalMask && i > query ? -99 : 0;
    return (dot + local + self) * state.attentionFocus + masked;
  });
  const probs = softmax(scores, 1);
  const top = topIndex(probs);
  return { scores, probs, topToken: ATTN_TOKENS[top].t };
}

function drawAttention(g, w, h, tab, t) {
  if (tab === "qkv") drawQKV(g, w, h);
  if (tab === "scores") drawScoreMatrix(g, w, h);
  if (tab === "mask") drawMask(g, w, h);
  if (tab === "heads") drawHeads(g, w, h, t);
}

function drawTokenRow(g, y, weights) {
  const pad = 26;
  const gap = 8;
  const bw = (canvas.getBoundingClientRect().width - pad * 2 - gap * (ATTN_TOKENS.length - 1)) / ATTN_TOKENS.length;
  ATTN_TOKENS.forEach((token, i) => {
    const x = pad + i * (bw + gap);
    const active = i === state.attentionQuery;
    const fill = active ? rgba(color.cyan, 0.16) : rgba(color.panel2, 0.88);
    const stroke = active ? color.cyan : color.line2;
    rect(g, x, y, bw, 38, 7, fill, stroke);
    label(g, token.t, x + bw / 2, y + 19, 12, active ? color.cyan : color.ink, "center");
    if (weights) label(g, weights[i].toFixed(2), x + bw / 2, y + 52, 10, color.faint, "center");
  });
}

function drawQKV(g, w, h) {
  const data = attentionData();
  const y = h - 102;
  drawAttentionArcs(g, y, data.probs);
  drawTokenRow(g, y, data.probs);
  const qx = 32;
  const qy = 50;
  title(g, "Query searches keys", qx, qy - 14, 18, color.ink);
  heat(g, qx, qy + 10, 260, 28, ATTN_TOKENS[state.attentionQuery].f, 1);
  label(g, "Q", qx + 280, qy + 24, 13, color.cyan);
  const kx = 32;
  const ky = 120;
  title(g, "Keys advertise content", kx, ky - 14, 16, color.muted);
  ATTN_TOKENS.forEach((token, i) => {
    heat(g, kx, ky + i * 28, 220, 18, token.f, 1);
    label(g, token.t, kx + 232, ky + i * 28 + 9, 10, i === data.probs.indexOf(Math.max(...data.probs)) ? color.green : color.faint);
  });
  const vx = Math.max(380, w * 0.55);
  title(g, "Weighted value mix", vx, 50, 18, color.ink);
  const mix = [0, 0, 0];
  ATTN_TOKENS.forEach((token, i) => token.f.forEach((value, k) => { mix[k] += value * data.probs[i]; }));
  heat(g, vx, 78, w - vx - 32, 32, mix, 1);
  label(g, `top key: ${data.topToken}`, vx, 126, 12, color.green);
}

function drawAttentionArcs(g, tokenY, probs) {
  const rect = canvas.getBoundingClientRect();
  const w = rect.width;
  const pad = 26;
  const gap = 8;
  const bw = (w - pad * 2 - gap * (ATTN_TOKENS.length - 1)) / ATTN_TOKENS.length;
  const qx = pad + state.attentionQuery * (bw + gap) + bw / 2;
  probs.forEach((p, i) => {
    if (p < 0.005 || i === state.attentionQuery) return;
    const tx = pad + i * (bw + gap) + bw / 2;
    const mid = (qx + tx) / 2;
    const height = 40 + Math.abs(i - state.attentionQuery) * 22;
    g.strokeStyle = rgba(color.cyan, Math.min(0.9, 0.12 + p * 2.5));
    g.lineWidth = 1 + p * 9;
    g.beginPath();
    g.moveTo(qx, tokenY);
    g.quadraticCurveTo(mid, tokenY - height, tx, tokenY);
    g.stroke();
  });
}

function drawScoreMatrix(g, w, h) {
  const n = ATTN_TOKENS.length;
  const size = Math.min(w - 76, h - 96);
  const x0 = 46;
  const y0 = 50;
  const cell = size / n;
  for (let q = 0; q < n; q += 1) {
    const prev = state.attentionQuery;
    state.attentionQuery = q;
    const data = attentionData(q);
    state.attentionQuery = prev;
    data.probs.forEach((p, k) => {
      const masked = state.causalMask && k > q;
      const fill = masked ? rgba(color.rose, 0.2) : rgba(color.cyan, 0.08 + p * 0.9);
      rect(g, x0 + k * cell, y0 + q * cell, cell - 1, cell - 1, 2, fill, null);
    });
  }
  g.strokeStyle = color.amber;
  g.lineWidth = 2;
  g.strokeRect(x0, y0 + state.attentionQuery * cell, size, cell);
  ATTN_TOKENS.forEach((token, i) => {
    label(g, token.t, x0 + i * cell + cell / 2, y0 - 16, 10, color.faint, "center");
    label(g, token.t, x0 - 10, y0 + i * cell + cell / 2, 10, color.faint, "right");
  });
  const x = x0 + size + 36;
  title(g, "Attention row", x, y0 + 20, 18, color.ink);
  const data = attentionData();
  drawBars(g, ATTN_TOKENS.map((t) => t.t), data.probs, x, y0 + 54, w - x - 32, 220, color.cyan, true);
}

function drawMask(g, w, h) {
  const n = ATTN_TOKENS.length;
  const x = 58;
  const y = 52;
  const size = Math.min(360, h - 100);
  const cell = size / n;
  title(g, "Causal visibility", x, y - 22, 18, color.ink);
  for (let q = 0; q < n; q += 1) {
    for (let k = 0; k < n; k += 1) {
      const allowed = k <= q;
      rect(g, x + k * cell, y + q * cell, cell - 1, cell - 1, 2, allowed ? rgba(color.green, 0.22) : rgba(color.rose, 0.18), null);
      label(g, allowed ? "1" : "0", x + k * cell + cell / 2, y + q * cell + cell / 2, 11, allowed ? color.green : color.rose, "center");
    }
  }
  const rx = x + size + 56;
  title(g, "Future tokens are hidden", rx, y + 12, 18, color.ink);
  g.font = "14px Segoe UI, system-ui, sans-serif";
  g.fillStyle = color.muted;
  wrapText(g, "Rows are query positions. Columns are keys. A value of 0 blocks attention to tokens that have not been generated yet.", rx, y + 42, w - rx - 42, 23, 5);
  drawTokenRow(g, h - 92, attentionData().probs);
}

function drawHeads(g, w, h, t) {
  const patterns = {
    local: [0.5, 1, 0.55, 0.18],
    syntax: [0.18, 0.52, 1, 0.35],
    entity: [1, 0.18, 0.42, 0.75],
    recency: [0.25, 0.55, 0.85, 1]
  };
  const names = Object.keys(patterns);
  const pad = 28;
  const headH = (h - 70) / names.length;
  names.forEach((name, row) => {
    const y = 34 + row * headH;
    const active = name === state.attentionHead;
    rect(g, pad, y, w - pad * 2, headH - 12, 8, active ? rgba(color.cyan, 0.08) : rgba(color.panel, 0.8), active ? color.cyan : color.line);
    title(g, name, pad + 16, y + 24, 15, active ? color.cyan : color.ink);
    const weights = ATTN_TOKENS.map((_, i) => {
      const base = patterns[name][Math.min(3, Math.abs(i - state.attentionQuery))] || 0.15;
      return base + 0.12 * Math.sin(t + i);
    });
    const probs = softmax(weights, 0.7);
    drawBars(g, ATTN_TOKENS.map((token) => token.t), probs, pad + 110, y + 18, w - pad * 2 - 130, headH - 48, active ? color.cyan : color.blue, false);
  });
}

function drawBlock(g, w, h, tab, t) {
  if (tab === "stream") drawBlockStream(g, w, h, t);
  if (tab === "norm") drawLayerNorm(g, w, h);
  if (tab === "mlp") drawMLP(g, w, h, t);
  if (tab === "stack") drawStack(g, w, h);
}

function residualVector(layer = state.blockLayer) {
  return Array.from({ length: 16 }, (_, i) => Math.sin(i * 0.8 + layer * 0.35) + 0.45 * Math.cos(i * 1.6 - layer));
}

function drawBlockStream(g, w, h, t) {
  const cx = w * 0.36;
  const top = 52;
  const bottom = h - 54;
  g.strokeStyle = rgba(color.cyan, 0.5);
  g.lineWidth = 3;
  g.beginPath();
  g.moveTo(cx, top);
  g.lineTo(cx, bottom);
  g.stroke();
  const blocks = [["Layer norm", color.green], ["Attention", color.blue], ["Add", color.cyan], ["Layer norm", color.green], ["MLP", color.amber], ["Add", color.cyan]];
  blocks.forEach(([name, c], i) => {
    const y = top + i * ((bottom - top) / (blocks.length - 1));
    rect(g, cx - 94, y - 20, 188, 40, 7, rgba(c, 0.1), c);
    label(g, name, cx, y, 12, c, "center");
  });
  const pulse = top + ((Math.sin(t * 1.6) + 1) / 2) * (bottom - top);
  g.fillStyle = color.cyan;
  g.beginPath();
  g.arc(cx, pulse, 8, 0, TAU);
  g.fill();
  const rx = Math.max(470, w * 0.58);
  title(g, `Residual stream after layer ${state.blockLayer}`, rx, 64, 18, color.ink);
  heat(g, rx, 92, w - rx - 32, 34, residualVector());
  label(g, "x = x + attention(x)", rx, 150, 12, color.muted);
  label(g, "x = x + MLP(x)", rx, 174, 12, color.muted);
  drawMiniTokens(g, rx, 230, w - rx - 32);
}

function drawMiniTokens(g, x, y, width) {
  const words = ["The", "bank", "was", "quiet"];
  const bw = (width - (words.length - 1) * 8) / words.length;
  words.forEach((word, i) => {
    rect(g, x + i * (bw + 8), y, bw, 34, 6, rgba(color.panel2, 0.9), i === 1 ? color.cyan : color.line2);
    label(g, word, x + i * (bw + 8) + bw / 2, y + 17, 12, i === 1 ? color.cyan : color.ink, "center");
  });
}

function drawLayerNorm(g, w, h) {
  const before = residualVector().map((v, i) => v * (1 + i / 20));
  const mean = before.reduce((a, b) => a + b, 0) / before.length;
  const centered = before.map((v) => (v - mean) * state.normStrength);
  const x = 48;
  title(g, "Normalize before the sublayer", x, 48, 20, color.ink);
  label(g, "before", x, 94, 12, color.faint);
  heat(g, x + 90, 80, w - 150, 32, before);
  label(g, "mean shift", x, 172, 12, color.faint);
  arrow(g, x + 120, 166, w - 92, 166, color.green, 2, 0.8);
  label(g, "after", x, 240, 12, color.faint);
  heat(g, x + 90, 226, w - 150, 32, centered);
  drawBars(g, ["mean", "variance", "scale"], [Math.abs(mean), 0.82, state.normStrength], x + 90, 306, Math.min(520, w - 160), 120, color.green, false);
}

function drawMLP(g, w, h, t) {
  const x = 44;
  const y = 64;
  title(g, "Feed-forward expansion", x, 38, 20, color.ink);
  const input = residualVector();
  const hidden = Array.from({ length: 28 }, (_, i) => Math.max(0, Math.sin(i * 0.47 + state.blockLayer) * state.mlpGain + 0.32 * Math.cos(t + i)));
  const output = Array.from({ length: 16 }, (_, i) => Math.sin(i * 0.68 + hidden[i] * 1.2) * 0.8);
  heat(g, x, y, w - x * 2, 26, input);
  label(g, "input vector", x, y - 16, 11, color.faint);
  arrow(g, w / 2, y + 42, w / 2, y + 84, color.amber, 2, 0.9);
  heat(g, x, y + 96, w - x * 2, 54, hidden);
  label(g, "expanded hidden activations", x, y + 82, 11, color.faint);
  arrow(g, w / 2, y + 168, w / 2, y + 210, color.amber, 2, 0.9);
  heat(g, x, y + 222, w - x * 2, 26, output);
  label(g, "projected update", x, y + 206, 11, color.faint);
  drawBars(g, ["off", "low", "mid", "high"], [0.12, 0.33, 0.61, Math.min(1, state.mlpGain / 1.8)], x, h - 146, Math.min(540, w - 88), 110, color.amber, false);
}

function drawStack(g, w, h) {
  const pad = 36;
  const n = 12;
  const bh = (h - 86) / n;
  title(g, "Repeated blocks", pad, 34, 20, color.ink);
  for (let i = 0; i < n; i += 1) {
    const y = 62 + i * bh;
    const active = i + 1 === state.blockLayer;
    rect(g, pad, y, 230, Math.max(24, bh - 6), 6, active ? rgba(color.cyan, 0.14) : color.panel, active ? color.cyan : color.line);
    label(g, `layer ${String(i + 1).padStart(2, "0")}`, pad + 18, y + (bh - 6) / 2, 12, active ? color.cyan : color.muted);
    label(g, "attn + MLP", pad + 190, y + (bh - 6) / 2, 11, color.faint, "right");
  }
  const x = 330;
  title(g, "Feature refinement", x, 72, 18, color.ink);
  for (let layer = 1; layer <= 12; layer += 1) {
    const vals = residualVector(layer);
    heat(g, x, 104 + (layer - 1) * 28, w - x - 36, 18, vals);
  }
}

const VOCAB = [
  { word: "mat", logit: 3.4 },
  { word: "rug", logit: 2.8 },
  { word: "floor", logit: 2.2 },
  { word: "table", logit: 1.3 },
  { word: "sofa", logit: 0.9 },
  { word: "grass", logit: 0.2 },
  { word: "quiet", logit: 1.1 },
  { word: "idea", logit: -0.3 },
  { word: "vector", logit: -0.8 },
  { word: "moon", logit: -1.1 }
];

function decodedProbs() {
  let probs = softmax(VOCAB.map((item) => item.logit), state.temperature);
  if (state.decoding === "greedy") {
    const top = topIndex(probs);
    probs = probs.map((_, i) => (i === top ? 1 : 0));
  } else if (state.decoding === "topk") {
    const keep = new Set([...probs.keys()].sort((a, b) => probs[b] - probs[a]).slice(0, state.topK));
    probs = normalize(probs.map((p, i) => (keep.has(i) ? p : 0)));
  } else {
    const order = [...probs.keys()].sort((a, b) => probs[b] - probs[a]);
    let acc = 0;
    const keep = new Set();
    for (const i of order) {
      keep.add(i);
      acc += probs[i];
      if (acc >= 0.9) break;
    }
    probs = normalize(probs.map((p, i) => (keep.has(i) ? p : 0)));
  }
  return probs;
}

function normalize(values) {
  const total = values.reduce((a, b) => a + b, 0) || 1;
  return values.map((v) => v / total);
}

function pickIndex(probs) {
  if (state.decoding === "greedy") return topIndex(probs);
  const r = seeded(state.sampleCursor + 11);
  let acc = 0;
  for (let i = 0; i < probs.length; i += 1) {
    acc += probs[i];
    if (r <= acc) return i;
  }
  return probs.length - 1;
}

function seeded(n) {
  return Math.abs(Math.sin(n * 12.9898) * 43758.5453) % 1;
}

function drawLogits(g, w, h, tab) {
  const logits = VOCAB.map((v) => v.logit);
  const probs = decodedProbs();
  if (tab === "projection") {
    title(g, "Final hidden state projected to vocabulary", 32, 44, 20, color.ink);
    heat(g, 32, 78, Math.min(520, w - 64), 34, residualVector(12));
    arrow(g, Math.min(560, w * 0.55), 95, Math.min(650, w * 0.64), 95, color.amber, 2, 0.9);
    drawBars(g, VOCAB.map((v) => v.word), logits, Math.min(660, w * 0.67), 52, Math.max(220, w - Math.min(660, w * 0.67) - 34), h - 104, color.violet, true);
  }
  if (tab === "softmax") {
    title(g, "Softmax distribution", 32, 42, 20, color.ink);
    drawBars(g, VOCAB.map((v) => v.word), probs, 34, 72, w - 68, h - 118, color.cyan, true);
  }
  if (tab === "decode") {
    title(g, `Decoder mode: ${state.decoding}`, 32, 42, 20, color.ink);
    drawBars(g, VOCAB.map((v) => v.word), probs, 34, 78, w - 68, h - 150, color.amber, true);
    const idx = pickIndex(probs);
    rect(g, 34, h - 82, w - 68, 44, 8, rgba(color.green, 0.12), color.green);
    label(g, `selected next token: ${VOCAB[idx].word}`, 54, h - 60, 14, color.green);
  }
  if (tab === "stream") {
    const base = ["The", "cat", "sat", "on", "the"];
    const idx = pickIndex(probs);
    const stream = [...base, VOCAB[idx].word];
    title(g, "Autoregressive stream", 32, 50, 20, color.ink);
    let x = 34;
    stream.forEach((token, i) => {
      const tw = 46 + token.length * 9;
      rect(g, x, 98, tw, 42, 7, i === stream.length - 1 ? rgba(color.green, 0.14) : color.panel, i === stream.length - 1 ? color.green : color.line2);
      label(g, token, x + tw / 2, 119, 13, i === stream.length - 1 ? color.green : color.ink, "center");
      x += tw + 9;
    });
    drawBars(g, VOCAB.map((v) => v.word), probs, 34, 202, w - 68, h - 250, color.cyan, true);
  }
}

function drawBars(g, labels, values, x, y, w, h, c = color.cyan, annotate = false) {
  const max = Math.max(0.001, ...values.map((v) => Math.abs(v)));
  const min = Math.min(0, ...values);
  const bw = w / values.length;
  const zero = min < 0 ? y + h * (max / (max - min)) : y + h;
  g.strokeStyle = color.line;
  g.beginPath();
  g.moveTo(x, zero);
  g.lineTo(x + w, zero);
  g.stroke();
  values.forEach((value, i) => {
    const px = x + i * bw + 4;
    const barH = min < 0 ? Math.abs(value) / (max - min) * h : Math.abs(value) / max * h;
    const py = value >= 0 ? zero - barH : zero;
    rect(g, px, py, Math.max(3, bw - 8), Math.max(2, barH), 3, rgba(c, 0.28 + 0.5 * Math.abs(value / max)), null);
    label(g, labels[i], x + i * bw + bw / 2, y + h + 18, 10, color.faint, "center");
    if (annotate) label(g, value < 1 ? value.toFixed(2) : value.toFixed(1), x + i * bw + bw / 2, py - 10, 10, color.muted, "center");
  });
}

function lossAt(step) {
  return 2.9 * Math.exp(-step / 48) + 0.16 + 0.04 * Math.sin(step * 0.29);
}

function gradNorm(step) {
  return 1.8 * Math.exp(-step / 62) + 0.06;
}

function drawTraining(g, w, h, tab, t) {
  if (tab === "loss") drawLoss(g, w, h);
  if (tab === "backprop") drawBackprop(g, w, h, t);
  if (tab === "opt") drawOptimizer(g, w, h);
  if (tab === "batch") drawBatches(g, w, h);
}

function drawLoss(g, w, h) {
  const x = 52;
  const y = 54;
  const gw = w - 100;
  const gh = h - 120;
  title(g, "Cross entropy falls with training", x, 32, 20, color.ink);
  g.strokeStyle = color.line2;
  g.beginPath();
  g.moveTo(x, y);
  g.lineTo(x, y + gh);
  g.lineTo(x + gw, y + gh);
  g.stroke();
  g.strokeStyle = color.cyan;
  g.lineWidth = 2;
  g.beginPath();
  for (let s = 0; s <= state.trainingStep; s += 1) {
    const px = x + (s / 160) * gw;
    const py = y + gh - (1 - Math.min(1, lossAt(s) / 3)) * gh;
    if (s === 0) g.moveTo(px, py);
    else g.lineTo(px, py);
  }
  g.stroke();
  const px = x + (state.trainingStep / 160) * gw;
  const py = y + gh - (1 - Math.min(1, lossAt(state.trainingStep) / 3)) * gh;
  g.fillStyle = color.cyan;
  g.beginPath();
  g.arc(px, py, 6, 0, TAU);
  g.fill();
  label(g, "loss", x + 6, y + 12, 11, color.faint);
  label(g, "optimizer steps", x + gw - 116, y + gh + 20, 11, color.faint);
}

function drawBackprop(g, w, h, t) {
  const nodes = [
    [w * 0.22, h * 0.35], [w * 0.22, h * 0.62],
    [w * 0.46, h * 0.28], [w * 0.46, h * 0.52], [w * 0.46, h * 0.74],
    [w * 0.72, h * 0.48]
  ];
  const edges = [[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [3, 5], [4, 5]];
  title(g, "Gradients flow backward", 36, 38, 20, color.ink);
  edges.forEach(([a, b]) => {
    const from = nodes[a];
    const to = nodes[b];
    arrow(g, from[0], from[1], to[0], to[1], color.line2, 1, 0.8);
    const p = (t * 1.7) % 1;
    const bx = to[0] + (from[0] - to[0]) * p;
    const by = to[1] + (from[1] - to[1]) * p;
    g.fillStyle = color.rose;
    g.beginPath();
    g.arc(bx, by, 4, 0, TAU);
    g.fill();
  });
  nodes.forEach((node, i) => {
    rect(g, node[0] - 22, node[1] - 22, 44, 44, 8, i === 5 ? rgba(color.cyan, 0.14) : color.panel, i === 5 ? color.cyan : color.line2);
    label(g, i === 5 ? "loss" : `w${i + 1}`, node[0], node[1], 12, i === 5 ? color.cyan : color.muted, "center");
  });
  label(g, "backward pass computes dLoss / dWeight", 36, h - 36, 13, color.rose);
}

function drawOptimizer(g, w, h) {
  const x = 46;
  const y = 58;
  const gw = w - 92;
  const gh = h - 118;
  title(g, "Optimizer step on a loss surface", x, 34, 20, color.ink);
  for (let i = 0; i < 90; i += 1) {
    const px = x + (i / 89) * gw;
    const val = Math.pow((i - 64) / 45, 2) + 0.14 * Math.sin(i * 0.34);
    const py = y + gh - Math.min(1, val / 2.2) * gh;
    if (i === 0) {
      g.beginPath();
      g.moveTo(px, py);
    } else {
      g.lineTo(px, py);
    }
  }
  g.strokeStyle = color.amber;
  g.lineWidth = 2;
  g.stroke();
  const pos = Math.max(10, 76 - state.trainingStep * state.learningRate * 8);
  const px = x + (pos / 89) * gw;
  const val = Math.pow((pos - 64) / 45, 2) + 0.14 * Math.sin(pos * 0.34);
  const py = y + gh - Math.min(1, val / 2.2) * gh;
  g.fillStyle = color.cyan;
  g.beginPath();
  g.arc(px, py, 7, 0, TAU);
  g.fill();
  arrow(g, px + 36, py - 20, px + 4, py - 2, color.cyan, 2, 0.9);
  label(g, `learning rate ${state.learningRate.toFixed(3)}`, x, h - 36, 12, color.muted);
}

function drawBatches(g, w, h) {
  title(g, "Batches average many examples", 34, 40, 20, color.ink);
  const cols = 4;
  const rows = state.batchSize;
  const pad = 34;
  const cellW = (w - pad * 2 - (cols - 1) * 10) / cols;
  const cellH = Math.min(56, (h - 120) / rows);
  for (let r = 0; r < rows; r += 1) {
    for (let c = 0; c < cols; c += 1) {
      const x = pad + c * (cellW + 10);
      const y = 78 + r * (cellH + 10);
      const loss = Math.max(0.08, lossAt(state.trainingStep + r * 7 + c * 3) + (seeded(r * 11 + c) - 0.5) * 0.22);
      rect(g, x, y, cellW, cellH, 7, rgba(loss > 1 ? color.rose : color.green, 0.12), loss > 1 ? color.rose : color.green);
      label(g, `seq ${r + 1}.${c + 1}`, x + 12, y + 18, 11, color.muted);
      label(g, loss.toFixed(2), x + cellW - 12, y + cellH - 17, 12, loss > 1 ? color.rose : color.green, "right");
    }
  }
  label(g, "batch loss = mean(sequence losses)", pad, h - 36, 12, color.faint);
}

function probeScore() {
  return Math.max(0.05, Math.min(0.98, 0.35 + state.repLayer / 24 + Math.abs(state.steering) * 0.12));
}

function drawRepresentations(g, w, h, tab, t) {
  if (tab === "map") drawFeatureMap(g, w, h);
  if (tab === "probe") drawProbe(g, w, h);
  if (tab === "steer") drawSteer(g, w, h);
  if (tab === "circuit") drawCircuit(g, w, h, t);
}

const FEATURES = [
  ["sentiment", [2, 4], color.rose],
  ["entity", [5, 3], color.green],
  ["syntax", [3, 7], color.blue],
  ["style", [7, 6], color.amber],
  ["topic", [8, 2], color.violet],
  ["instruction", [5.8, 7.8], color.cyan]
];

function featureTransform(w, h) {
  const pad = 52;
  return {
    mx: (p) => pad + (p[0] / 10) * (w - pad * 2),
    my: (p) => h - pad - (p[1] / 10) * (h - pad * 2)
  };
}

function drawFeatureMap(g, w, h) {
  const { mx, my } = featureTransform(w, h);
  title(g, `Activation space at layer ${state.repLayer}`, 34, 38, 20, color.ink);
  FEATURES.forEach(([name, p, c]) => {
    const radius = 34 + state.repLayer * 1.4;
    g.fillStyle = rgba(c, 0.1);
    g.beginPath();
    g.arc(mx(p), my(p), radius, 0, TAU);
    g.fill();
    g.strokeStyle = rgba(c, 0.5);
    g.stroke();
    g.fillStyle = c;
    g.beginPath();
    g.arc(mx(p), my(p), 5, 0, TAU);
    g.fill();
    label(g, name, mx(p), my(p) - 16, 12, c, "center");
  });
  const pos = [4 + state.steering, 5.2 + state.repLayer / 12];
  rect(g, mx(pos) - 8, my(pos) - 8, 16, 16, 4, color.ink, null);
  label(g, "current state", mx(pos) + 16, my(pos), 12, color.ink);
}

function drawProbe(g, w, h) {
  title(g, `Linear probe: ${state.probe}`, 34, 42, 20, color.ink);
  const names = ["layer 1", "layer 4", "layer 8", "layer 12", "layer 16"];
  const values = names.map((_, i) => Math.min(0.96, 0.18 + i * 0.14 + (state.probe.length % 4) * 0.04 + state.steering * 0.03));
  drawBars(g, names, values, 42, 92, w - 84, h - 170, color.green, true);
  label(g, "A simple classifier can often read information from hidden states before the final layer.", 42, h - 52, 12, color.muted);
}

function drawSteer(g, w, h) {
  title(g, "Adding a steering direction", 34, 42, 20, color.ink);
  const x = 42;
  const y = 92;
  heat(g, x, y, w - 84, 28, residualVector(state.repLayer));
  label(g, "original activation", x, y - 16, 11, color.faint);
  const steered = residualVector(state.repLayer).map((v, i) => v + state.steering * Math.sin(i * 0.7));
  heat(g, x, y + 98, w - 84, 28, steered);
  label(g, "after adding direction", x, y + 82, 11, color.faint);
  const probs = normalize([0.22 + state.steering * 0.12, 0.18, 0.26 - state.steering * 0.08, 0.16, 0.18]);
  drawBars(g, ["formal", "direct", "warm", "terse", "plain"], probs, x, y + 180, w - 84, h - y - 228, color.amber, true);
}

function drawCircuit(g, w, h, t) {
  title(g, "A small feature circuit", 34, 42, 20, color.ink);
  const nodes = [
    ["token", 0.16, 0.58, color.cyan],
    ["name", 0.34, 0.32, color.green],
    ["syntax", 0.36, 0.72, color.blue],
    ["relation", 0.58, 0.48, color.amber],
    ["logit", 0.78, 0.58, color.rose]
  ];
  const edges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]];
  edges.forEach(([a, b], i) => {
    const from = nodes[a];
    const to = nodes[b];
    arrow(g, from[1] * w, from[2] * h, to[1] * w, to[2] * h, i === 3 ? color.blue : color.line2, 2, 0.85);
    const p = (t * 0.8 + i * 0.17) % 1;
    g.fillStyle = color.cyan;
    g.beginPath();
    g.arc((from[1] + (to[1] - from[1]) * p) * w, (from[2] + (to[2] - from[2]) * p) * h, 4, 0, TAU);
    g.fill();
  });
  nodes.forEach(([name, nx, ny, c]) => {
    rect(g, nx * w - 44, ny * h - 22, 88, 44, 8, rgba(c, 0.12), c);
    label(g, name, nx * w, ny * h, 12, c, "center");
  });
}

function fieldNoteScores() {
  const riskByScenario = {
    debug: "wrong frame",
    ship: "silent failure",
    teach: "false simplicity",
    eval: "bad proxy"
  };
  const leverByScenario = {
    debug: "isolate variables",
    ship: "tight evals",
    teach: "one clean model",
    eval: "real examples"
  };
  return {
    topRisk: riskByScenario[state.noteScenario] || "ambiguity",
    shipLever: leverByScenario[state.noteScenario] || "feedback"
  };
}

function drawFieldNotes(g, w, h, tab, t) {
  if (tab === "mental") drawFieldMental(g, w, h, t);
  if (tab === "traps") drawFieldTraps(g, w, h);
  if (tab === "production") drawFieldProduction(g, w, h);
  if (tab === "debug") drawFieldDebug(g, w, h, t);
}

const FIELD_MENTAL = [
  ["Prompt", "The prompt is a control surface. It sets task, context, constraints, and the first distribution the model must inhabit.", color.cyan],
  ["State", "The model compresses that prompt into activations. The final state is the thing that makes one next token easier than another.", color.green],
  ["Policy", "Sampling is a behavior policy layered on top of logits. Temperature and filtering change the personality of the next-token loop.", color.amber],
  ["Loop", "Generation is not one answer. It is repeated prediction, with each new token becoming fresh context for the next decision.", color.violet],
  ["Ground", "External tools, retrieval, tests, and user feedback are how the system reconnects fluent text to the world.", color.rose]
];

function drawFieldMental(g, w, h, t) {
  const pad = 34;
  title(g, "My working mental model", pad, 42, 20, color.ink);
  const visible = Math.min(FIELD_MENTAL.length, state.noteDepth);
  const flowY = 96;
  const gap = 12;
  const bw = (w - pad * 2 - gap * (FIELD_MENTAL.length - 1)) / FIELD_MENTAL.length;
  FIELD_MENTAL.forEach(([name, body, c], i) => {
    const active = i < visible;
    const x = pad + i * (bw + gap);
    rect(g, x, flowY, bw, 74, 8, active ? rgba(c, 0.12) : color.panel, active ? c : color.line);
    label(g, String(i + 1).padStart(2, "0"), x + 14, flowY + 20, 11, active ? c : color.faint);
    title(g, name, x + 14, flowY + 48, 15, active ? c : color.muted);
    if (i < FIELD_MENTAL.length - 1) arrow(g, x + bw + 2, flowY + 37, x + bw + gap - 2, flowY + 37, active ? c : color.line2, 1.6, 0.85);
  });

  const cardY = 212;
  const cardH = h - cardY - 32;
  FIELD_MENTAL.slice(0, visible).forEach(([name, body, c], i) => {
    const cardW = (w - pad * 2 - 14 * (visible - 1)) / visible;
    const x = pad + i * (cardW + 14);
    rect(g, x, cardY, cardW, cardH, 8, rgba(c, 0.08), rgba(c, 0.55));
    title(g, name, x + 18, cardY + 30, 16, c);
    g.font = "13px Segoe UI, system-ui, sans-serif";
    g.fillStyle = color.muted;
    wrapText(g, body, x + 18, cardY + 58, cardW - 36, 22, 8);
  });

  const pulseX = pad + ((Math.sin(t * 0.9) + 1) / 2) * (w - pad * 2);
  g.fillStyle = color.cyan;
  g.beginPath();
  g.arc(pulseX, flowY + 94, 4, 0, TAU);
  g.fill();
}

const FIELD_TRAPS = [
  ["Attention is not explanation", "Attention weights are useful clues, but a causal explanation needs intervention, ablation, or counterfactual tests.", color.blue],
  ["Confidence is not truth", "A high-probability token can still be wrong when the prompt lacks evidence or asks for a brittle fact.", color.rose],
  ["Embeddings are not dictionaries", "Meaning is contextual and distributed. A nearest neighbor plot is a flashlight, not the room.", color.violet],
  ["Long context is not memory", "More tokens can help, but retrieval quality, ordering, and distraction often dominate raw window size.", color.amber],
  ["Prompting is not product design", "A prompt can guide behavior, but stable systems need constraints, evals, tools, and recovery paths.", color.green]
];

function drawFieldTraps(g, w, h) {
  const pad = 30;
  title(g, "Traps I try not to fall into", pad, 40, 20, color.ink);
  const visible = Math.min(FIELD_TRAPS.length, state.noteDepth);
  const cols = w > 820 ? 3 : 2;
  const gap = 14;
  const cardW = (w - pad * 2 - gap * (cols - 1)) / cols;
  const cardH = Math.min(142, (h - 94) / Math.ceil(visible / cols) - gap);
  FIELD_TRAPS.slice(0, visible).forEach(([name, body, c], i) => {
    const x = pad + (i % cols) * (cardW + gap);
    const y = 80 + Math.floor(i / cols) * (cardH + gap);
    rect(g, x, y, cardW, cardH, 8, rgba(c, 0.09), rgba(c, 0.55));
    title(g, name, x + 16, y + 26, 15, c);
    g.font = "12.5px Segoe UI, system-ui, sans-serif";
    g.fillStyle = color.muted;
    wrapText(g, body, x + 16, y + 48, cardW - 32, 20, 4);
    const meter = 0.35 + ((i + state.noteDepth) % 4) * 0.16;
    rect(g, x + 16, y + cardH - 24, cardW - 32, 7, 999, "#07080d", color.line);
    rect(g, x + 16, y + cardH - 24, (cardW - 32) * meter, 7, 999, c, null);
  });
  const scores = fieldNoteScores();
  label(g, `scenario: ${state.noteScenario}  |  watch for: ${scores.topRisk}`, pad, h - 28, 12, color.faint);
}

function drawFieldProduction(g, w, h) {
  const pad = 34;
  title(g, "Production lesson: inference is a budget", pad, 42, 20, color.ink);
  const budget = state.latencyBudget;
  const costs = [
    ["route", Math.max(12, budget * 0.08), color.violet],
    ["retrieve", Math.max(20, budget * 0.16), color.green],
    ["prefill", Math.max(26, budget * 0.22 + state.noteDepth * 8), color.blue],
    ["decode", Math.max(30, budget * 0.34 + state.noteDepth * 10), color.cyan],
    ["verify", Math.max(14, budget * 0.12), color.amber]
  ];
  const total = costs.reduce((sum, [, ms]) => sum + ms, 0);
  let x = pad;
  const y = 104;
  const usable = w - pad * 2;
  costs.forEach(([name, ms, c]) => {
    const bw = Math.max(56, usable * (ms / total));
    rect(g, x, y, bw - 6, 72, 7, rgba(c, 0.12), c);
    label(g, name, x + 14, y + 24, 12, c);
    label(g, `${Math.round(ms)} ms`, x + 14, y + 50, 12, color.ink);
    x += bw;
  });

  const rows = [
    ["KV cache", "Keeps previous keys and values so decoding new tokens does not recompute the whole prefix.", color.cyan],
    ["Context quality", "Relevant, ordered context beats a giant unfocused prompt more often than people expect.", color.green],
    ["Streaming", "First-token latency matters psychologically; stream once the answer path is stable enough.", color.amber],
    ["Evals", "A model upgrade is not real until the important examples still pass.", color.rose]
  ];
  const rowY = 228;
  rows.forEach(([name, body, c], i) => {
    const yy = rowY + i * 66;
    rect(g, pad, yy, w - pad * 2, 52, 7, rgba(c, 0.07), color.line);
    title(g, name, pad + 18, yy + 18, 14, c);
    g.font = "12.5px Segoe UI, system-ui, sans-serif";
    g.fillStyle = color.muted;
    wrapText(g, body, pad + 150, yy + 11, w - pad * 2 - 170, 19, 2);
  });
  label(g, `estimated path: ${Math.round(total)} ms  |  target knob: ${budget} ms/token`, pad, h - 28, 12, total > budget * 1.25 ? color.rose : color.green);
}

function drawFieldDebug(g, w, h, t) {
  const pad = 34;
  title(g, "Debug loop for surprising outputs", pad, 42, 20, color.ink);
  const nodes = [
    ["1", "Frame", "What task did the prompt actually specify?", 0.18, 0.28, color.cyan],
    ["2", "Evidence", "Did the answer have enough grounded context?", 0.5, 0.22, color.green],
    ["3", "Decode", "Did sampling make a rare path likely?", 0.82, 0.28, color.amber],
    ["4", "Check", "Can a tool, eval, or counterexample catch it?", 0.68, 0.68, color.rose],
    ["5", "Tighten", "Change one variable and rerun the case.", 0.32, 0.7, color.violet]
  ];
  const edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]];
  edges.forEach(([a, b], i) => {
    const from = nodes[a];
    const to = nodes[b];
    const x1 = from[3] * w;
    const y1 = from[4] * h;
    const x2 = to[3] * w;
    const y2 = to[4] * h;
    arrow(g, x1, y1, x2, y2, color.line2, 2, 0.85);
    const p = (t * 0.55 + i * 0.18) % 1;
    g.fillStyle = color.cyan;
    g.beginPath();
    g.arc(x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, 4, 0, TAU);
    g.fill();
  });
  nodes.forEach(([num, name, body, nx, ny, c]) => {
    const x = nx * w;
    const y = ny * h;
    rect(g, x - 86, y - 46, 172, 92, 8, rgba(c, 0.11), c);
    label(g, num, x - 66, y - 24, 12, c);
    title(g, name, x - 38, y - 24, 15, c);
    g.font = "12px Segoe UI, system-ui, sans-serif";
    g.fillStyle = color.muted;
    wrapText(g, body, x - 66, y + 2, 132, 18, 3);
  });
  const scores = fieldNoteScores();
  label(g, `best next move for ${state.noteScenario}: ${scores.shipLever}`, pad, h - 28, 12, color.green);
}

render();
requestAnimationFrame(animationLoop);
