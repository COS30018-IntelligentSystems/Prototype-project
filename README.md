## RAG-based cyber defence assistant

This project implements a retrieval-augmented generation (RAG) system focused on
MITRE ATT&CK techniques and CTI enrichment (AlienVault OTX). It is organised as
a small, production-lean Python package (`rag_system`) with a CLI interface and
offline index build scripts.

### Key components

- **MITRE ingestion and index**
  - Markdown MITRE ATT&CK files under `data/`.
  - Ingestion pipeline in `rag_system/ingestion/`:
    - `mitre_loader.py` – load and normalise metadata (technique ID & name).
    - `chunking.py` – header-aware + size-controlled text splitting.
    - `index_builder.py` – builds a ChromaDB collection with provenance and an
      `ingestion_manifest.json` for traceability.
- **Retriever**
  - ChromaDB persistent store via `rag_system/retrieval/vector_store.py`.
  - Query logic and optional filters in `rag_system/retrieval/retriever.py`.
  - Simple reranker hook in `rag_system/retrieval/reranker.py`.
- **LLM layer**
  - OpenRouter-backed OpenAI client in `rag_system/llm/client.py`.
  - Prompt templates in `rag_system/llm/prompts.py`.
  - MITRE-aware answer generator in `rag_system/llm/mitre_answerer.py`.
- **Agents and multi-agent routing**
  - Input classification in `rag_system/agents/router.py`.
  - Query rewriting in `rag_system/agents/query_rewriter.py`.
  - MITRE RAG orchestration in `rag_system/agents/mitre_agent.py`.
  - OTX CTI wrapper in `rag_system/agents/otx_agent.py`.
  - Minimal in-memory history in `rag_system/agents/conversation_manager.py`.
- **CLI and scripts**
  - Interactive CLI in `rag_system/cli/main.py`.
  - Index build / verify scripts under `scripts/`.

The high-level flow matches your RAG diagram: user input → router (input type) →
query rewriter → global retriever (Chroma) → answerer → conversation manager →
CLI response.

### Setup

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set:
   - `OPENROUTER_API_KEY`
   - `OTX_API_KEY`

### Building and verifying the index

From the `RAG/` directory:

```bash
python scripts/build_index.py
python scripts/verify_index.py
```

or, using the helper script on Windows PowerShell:

```powershell
.\tasks.ps1 build-index
.\tasks.ps1 verify-index
```

### Running the CLI

From `RAG/`:

```bash
python -m rag_system.cli.main
```

or:

```powershell
.\tasks.ps1 run-cli
```

You can paste:

- MITRE technique IDs (for example `T1047`),
- system log snippets,
- IP addresses or file hashes (for OTX enrichment).

The system will classify the input, route to the appropriate agent, and return
structured JSON with MITRE technique details and/or CTI information.

### Tests

Basic tests live in `tests/` and can be run with:

```bash
pytest
```

or:

```powershell
.\tasks.ps1 run-tests
```

