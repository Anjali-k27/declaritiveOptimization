# Newton SkillUP AlphaFund OS

A local Streamlit intelligence dashboard powered by DSPy and Google Gemini. It simulates a multi-source data retrieval pipeline (SQL, vector search, graph database) and synthesizes all three outputs into a formal executive summary using a structured language model chain.

---

## Architecture Overview

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│              Trinity Pipeline               │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  SQL /   │  │  FAISS   │  │  Neo4j   │  │
│  │  Math    │  │  Vector  │  │  Graph   │  │
│  │ Context  │  │  Store   │  │   DB     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       └─────────────┴─────────────┘         │
│                      │                      │
│                      ▼                      │
│        DSPy ChainOfThought Module           │
│        (AlphaFundExecutiveSynthesizer)      │
│                      │                      │
│                      ▼                      │
│              Executive Summary              │
│            + AI Reasoning Trace             │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
pythonProject1/
├── .env                  # API key (never commit this)
├── .gitignore
├── requirements.txt      # Python dependencies
├── synthesis_engine.py   # DSPy pipeline and LM configuration
├── app.py                # Streamlit dashboard UI
└── test_engine.py        # Automated pass/fail verification script
```

---

## Step-by-Step Breakdown

### Step 1 — Dependencies (`requirements.txt`)

Three packages drive the entire project:

| Package | Role |
|---|---|
| `streamlit` | Web UI framework — renders the dashboard in the browser |
| `dspy-ai` | DSPy framework — structures LLM calls as typed, composable modules |
| `python-dotenv` | Loads environment variables from the `.env` file at runtime |

Install with:
```bash
pip install -r requirements.txt
```

---

### Step 2 — The Engine (`synthesis_engine.py`)

This is the core of the project. It defines how the language model is instructed and invoked.

#### DSPy Signature: `AlphaFundExecutiveSynthesizer`

A DSPy `Signature` is a typed contract that tells the LLM exactly what inputs to expect and what output to produce. It replaces brittle hand-written prompt strings with a structured, testable interface.

```python
class AlphaFundExecutiveSynthesizer(dspy.Signature):
    """You are a senior investment analyst..."""
    sql_math_context: str        = dspy.InputField(...)
    faiss_document_context: str  = dspy.InputField(...)
    neo4j_relational_context: str = dspy.InputField(...)
    user_query: str              = dspy.InputField(...)
    executive_summary: str       = dspy.OutputField(...)
```

- **`sql_math_context`** — Quantitative financial data (e.g. market caps, valuations)
- **`faiss_document_context`** — Qualitative intelligence retrieved from a vector document store
- **`neo4j_relational_context`** — Graph database relationships showing competitive positioning
- **`user_query`** — The analyst's strategic question
- **`executive_summary`** — The LLM's synthesized 2–3 paragraph formal output

The docstring acts as the system prompt, instructing the model to weave all three data sources into a single coherent narrative.

#### DSPy Module: `DashboardPipeline`

A DSPy `Module` is the execution unit. It wires the signature into a specific prompting strategy:

```python
class DashboardPipeline(dspy.Module):
    def __init__(self):
        self.synthesize = dspy.ChainOfThought(AlphaFundExecutiveSynthesizer)
```

`dspy.ChainOfThought` automatically injects a hidden `reasoning` step before the model produces its final answer. This forces the model to think through its plan before writing, which significantly improves output quality and consistency.

#### LM Configuration

```python
lm = dspy.LM(model="gemini/gemini-2.5-flash", temperature=0.0)
dspy.configure(lm=lm)
```

- Model: **Google Gemini 2.5 Flash** — fast, capable, cost-efficient
- Temperature `0.0` — fully deterministic output, essential for repeatable financial analysis

#### API Key Mapping

```python
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")
```

`python-dotenv` reads `GEMINI_API_KEY` from `.env`. It is then re-mapped to `GOOGLE_API_KEY`, which is what the underlying `litellm` library (used by DSPy) expects when routing calls to the Gemini API.

#### Singleton

```python
master_synthesis_node = DashboardPipeline()
```

A single module instance is created at import time and shared across both `app.py` and `test_engine.py`. This avoids redundant initialisation and ensures consistent LM configuration.

---

### Step 3 — The Dashboard UI (`app.py`)

A Streamlit application that exposes the pipeline through a browser interface.

```
┌───────────────────────────────────────────────┐
│       Newton SkillUP AlphaFund OS             │
│                                               │
│  Strategic Query: [_________________________] │
│                                               │
│  [ Execute Trinity Pipeline ]                 │
│                                               │
│  ### Executive Summary                        │
│  ┌─────────────────────────────────────────┐  │
│  │  Alpha AI occupies a strategically...   │  │
│  └─────────────────────────────────────────┘  │
│                                               │
│  🔍 View AI Reasoning Trace (Audit Log) ▶     │
└───────────────────────────────────────────────┘
```

**Flow when the button is clicked:**

1. Three simulated retrieval strings are defined (standing in for live SQL, FAISS, and Neo4j calls)
2. They are passed alongside the user's query into `master_synthesis_node()`
3. The resulting `executive_summary` is rendered in a blue `st.info` block
4. The model's internal `reasoning` trace is available in a collapsible expander for audit purposes

The reasoning trace is the ChainOfThought output — it shows exactly how the model planned its response before writing, serving as an explainability and audit log.

---

### Step 4 — Verification (`test_engine.py`)

A standalone test script that validates the pipeline without launching the UI.

It uses the same simulated data as `app.py` and applies four strict pass/fail checks:

| Check | What it verifies |
|---|---|
| Microsoft $3.1T valuation | Financial context from SQL was incorporated |
| Satya Nadella acquisition interest | Qualitative intelligence from FAISS was incorporated |
| NeuralNet Labs competition | Graph relationship from Neo4j was incorporated |
| Rationale generated | ChainOfThought reasoning step executed successfully |

If any check fails, the signature description is tightened and the test is re-run until all four pass.

The exact query and simulated data used in the test:

```python
raw_sql   = "Microsoft Market Cap: $3.1T."
raw_faiss = "Satya Nadella considers Alpha AI a critical acquisition."
raw_neo4j = "(Alpha AI)--[COMPETES_WITH]--(NeuralNet Labs)"
query     = "Provide an overview of Alpha AI's market position."
```

Run it with:
```bash
python test_engine.py
```

---

## Setup & Usage

### 1. Clone and install
```bash
pip install -r requirements.txt
```

### 2. Configure your API key

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a free key at: https://aistudio.google.com/app/apikey

### 3. Run the verification test
```bash
python test_engine.py
```

Expected output:
```
[PASS] Microsoft $3.1T valuation
[PASS] Satya Nadella acquisition interest
[PASS] NeuralNet Labs competition
[PASS] Rationale generated

RESULT: ALL CHECKS PASSED - Pipeline is verified.
```

### 4. Launch the dashboard
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### 5. Try this query in the UI

Paste the following into the **Strategic Query** field and click **Execute Trinity Pipeline**:

```
Provide an overview of Alpha AI's market position.
```

**Expected Executive Summary output:**

> Alpha AI occupies a strategically critical position within the artificial intelligence sector, underscored by the explicit interest from industry titans. Microsoft CEO Satya Nadella has identified Alpha AI as a "critical acquisition," signaling its profound importance to the future strategic direction of major technology firms. This assessment is particularly significant given Microsoft's formidable market capitalization of $3.1 trillion, which illustrates the substantial financial capacity and strategic intent that could be brought to bear in pursuing such an acquisition, thereby validating Alpha AI's perceived value and technological leadership.
>
> The company's market position is further defined by its competitive landscape. Alpha AI is actively engaged in direct competition with NeuralNet Labs, as evidenced by the relational graph data. This competitive dynamic suggests that Alpha AI operates in a contested but high-growth segment, where innovation and strategic differentiation against key rivals like NeuralNet Labs are paramount for securing and expanding market share. The confluence of strong strategic interest from major players and a clear competitive environment positions Alpha AI as a pivotal entity within the evolving AI ecosystem.

**Expected Reasoning Trace (Audit Log):**

> The user requires a strategic executive summary on Alpha AI's market position. To fulfill this, I must synthesize information from all three provided contexts: the quantitative financial data (Microsoft's market cap), the qualitative intelligence (Satya Nadella's view on Alpha AI), and the relational graph data (Alpha AI's competitive relationship with NeuralNet Labs). The summary must explicitly reference each of these data points, maintain a formal tone, and be 2–3 paragraphs in length.
>
> My plan is to:
> 1. Begin by highlighting Alpha AI's strategic significance, drawing directly from Satya Nadella's assessment.
> 2. Contextualize this significance within the broader financial landscape, using Microsoft's substantial market capitalization ($3.1T) to illustrate the scale of potential strategic interest.
> 3. Conclude by detailing Alpha AI's competitive standing, specifically identifying NeuralNet Labs as a direct competitor as indicated by the relational graph data.
> 4. Ensure seamless integration of all three data points into a cohesive and authoritative narrative.

---

## Key Concepts

**DSPy** replaces hand-crafted prompt strings with typed Python modules. Prompts become signatures with defined inputs and outputs — testable, composable, and optimisable without touching the underlying LLM calls.

**ChainOfThought** is a DSPy prompting strategy that elicits a reasoning trace before the final answer. It improves output quality on synthesis tasks by forcing the model to plan before it writes.

**Trinity Pipeline** refers to the three simulated data retrieval layers:
- SQL/Math — structured quantitative data
- FAISS — unstructured document retrieval via vector similarity search
- Neo4j — graph-structured relational data

In a production deployment each layer would connect to a live database. In this build they are simulated strings, keeping the focus on the synthesis and reasoning layer.