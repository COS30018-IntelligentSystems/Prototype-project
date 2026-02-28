# RAG-based Cyber Defence Assistant

## Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** designed to enhance cyber defence capabilities by providing intelligent, context-aware intelligence on adversary tactics and techniques. The system integrates:

- **MITRE ATT&CK Framework**: A comprehensive dataset of adversary tactics and techniques
- **Cyber Threat Intelligence (CTI)**: Real-time enrichment via AlienVault OTX for indicators of compromise (IoCs) like IP addresses, file hashes, and domains
- **Advanced LLM Integration**: Powered by OpenRouter using state-of-the-art language models for natural language understanding and generation

Built as a lightweight, production-ready Python package with a clean CLI interface and offline processing capabilities.

## Purpose & Main Use Cases

The system is designed to:

1. **Technique Lookups**: Quickly retrieve detailed information about MITRE ATT&CK techniques (e.g., `T1047` - Windows Management Instrumentation)
2. **Log Analysis**: Analyze system logs and suspicious activity descriptions to identify relevant attack techniques and indicators
3. **IoC Enrichment**: Automatically enrich indicators of compromise (IP addresses, file hashes, domains) with threat intelligence from OTX
4. **Intelligent Conversation**: Maintain context across multiple queries within a session with conversation history support

### Example Scenarios

- **Security Analyst**: Paste suspicious PowerShell logs → System identifies relevant tactics and linked TTPs
- **Incident Response**: Input detected file hash → OTX enrichment reveals malware signatures and command & control IPs
- **Threat Intel**: Query attack techniques → Detailed MITRE ATT&CK information with contextual analysis

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT (CLI)                         │
│  - MITRE Technique IDs (T1047)                               │
│  - Log Snippets / Suspicious Activity                        │
│  - IoCs (IPs, File Hashes, Domains)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  ROUTER / CLASSIFIER   │
        │ (Input Type Detection) │
        └────────┬───────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐ ┌───────────┐ ┌──────────┐
│ MITRE   │ │MITRE LOGS │ │OTX / IOC │
│QUERY    │ │ ANALYSIS  │ │ENRICHMENT│
│AGENT    │ │ AGENT     │ │AGENT     │
└────┬────┘ └─────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┴────────────┘
            │
            ▼
    ┌──────────────────┐
    │ QUERY REWRITER   │
    │ (Intent Clarity) │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────────┐
    │  VECTOR RETRIEVER        │
    │  (ChromaDB - MITRE data) │
    └────────┬─────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ LLM ANSWERER     │
    │ (Generate Reply) │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ CONVERSATION MGR │
    │ (Session Memory) │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ CLI RESPONSE     │
    │ (JSON Output)    │
    └──────────────────┘
```

## Project Structure

```
RAG/
├── rag_system/                    # Main Python package
│   ├── agents/                    # Multi-agent routing & decision logic
│   │   ├── router.py              # Classify input type
│   │   ├── query_rewriter.py      # Clarify intent
│   │   ├── mitre_agent.py         # MITRE technique handling
│   │   ├── otx_agent.py           # OTX CTI enrichment
│   │   └── conversation_manager.py# Session history
│   ├── ingestion/                 # Data pipeline
│   │   ├── mitre_loader.py        # Parse MITRE markdown files
│   │   ├── chunking.py            # Intelligent text splitting
│   │   └── index_builder.py       # Build ChromaDB index
│   ├── retrieval/                 # Vector search
│   │   ├── vector_store.py        # ChromaDB wrapper
│   │   ├── retriever.py           # Query logic & filtering
│   │   └── reranker.py            # Result ranking
│   ├── llm/                       # Language model integration
│   │   ├── client.py              # OpenRouter OpenAI client
│   │   ├── prompts.py             # Prompt templates
│   │   └── mitre_answerer.py      # MITRE-specific response generation
│   ├── cli/
│   │   └── main.py                # Interactive CLI interface
│   ├── config.py                  # Configuration management
│   ├── data_models.py             # Pydantic data structures
│   ├── logging_config.py          # Logging setup
│   └── preprocessing/             # Data preprocessing utilities
├── data/                          # MITRE ATT&CK markdown documents
│   ├── T1001_Data_Obfuscation.md
│   ├── T1003_OS_Credential_Dumping.md
│   └── ... (100+ technique files)
├── chroma_db/                     # Persistent vector database
│   └── (auto-generated, contains embeddings)
├── scripts/                       # Utility scripts
│   ├── build_index.py             # Build/rebuild ChromaDB index
│   └── verify_index.py            # Verify index integrity
├── tests/                         # Unit tests
├── requirements.txt               # Python dependencies
├── .env                           # API keys (not in repo)
└── README.md                      # This file
```

## Installation & Setup

### 1. Create Virtual Environment (Recommended)

**Requirement**: Python 3.12 or lower is recommended for compatibility with all dependencies.

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Copy `.env.example` to `.env` and set:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OTX_API_KEY=your_otx_api_key_here
```

Obtain keys from:
- **OpenRouter**: https://openrouter.ai (free tier available)
- **AlienVault OTX**: https://otx.alienvault.com (free tier available)

## Building the Vector Index

Before running the CLI, you must build the ChromaDB index from MITRE ATT&CK markdown files.

### ⚠️ Important: Set PYTHONPATH on Windows

When running scripts on Windows, you **must** set `PYTHONPATH` to resolve module imports correctly:

```bash
# Windows (cmd)
set PYTHONPATH=.

# Windows (PowerShell)
$env:PYTHONPATH = "."

# macOS/Linux (bash/zsh)
export PYTHONPATH=.
```

### Build & Verify Steps

```bash
# Build the index from MITRE markdown files
python scripts/build_index.py

# Verify index integrity
python scripts/verify_index.py
```

This creates:
- `chroma_db/` directory with vector embeddings
- `chroma_db/ingestion_manifest.json` with metadata and traceability

## Running the CLI

### Interactive Mode

```bash
python -m rag_system.cli.main
```

The system will start an interactive session where you can input:

#### Input Examples

**MITRE Technique Query:**
```
T1047
```
→ Returns detailed information, detection methods, and mitigation strategies for Windows Management Instrumentation

**Log Snippet:**
```
Process spawned: cmd.exe with arguments "/c whoami" from svchost.exe
```
→ Identifies potential techniques (Command Execution, Credential Discovery) with risk assessment

**IoC Enrichment:**
```
192.168.1.100
```
→ Retrieves OTX threat intelligence: domain reputation, known malware C2, attack campaigns

**Natural Language Query:**
```
What are the techniques used for persistence on Windows systems?
```
→ Searches MITRE knowledge base and provides comprehensive list with examples

### Sample Interaction

```

{
  "mitre",
  "technique": {
    "id": "T1047",
    "name": "Windows Management Instrumentation",
    "description": "...",
    "detection": "...",
    "mitigation": "..."
  },
  "context_score": 0.95
}

> 192.168.1.100
{
  "type": "ioc_enrichment",
  "ioc_type": "ip_address",
  "otx_results": {
    "pulses": [...],
    "reputation": "suspicious",
    "last_seen": "2026-02-28"
  }
}

```

### Output Format

Responses are formatted as structured JSON containing:
- **technique_details**: MITRE ATT&CK metadata, detection rules, mitigations
- **otx_enrichment**: Threat intelligence from AlienVault OTX
- **context**: Relevance scores, source documents
- **timestamp**: When the query was processed

## Testing

Run unit tests to verify system integrity:

```bash
set PYTHONPATH=.
pytest
```

or with verbose output:

```bash
set PYTHONPATH=.
pytest -v
```

```powershell
.\tasks.ps1 run-tests
```

