## Cyber Threat Explainer Agent – Prototype (V1)

### 104988294 – Do Gia Huy

This prototype is an individual research project developed prior to the full COS30018 Option D group assignment.  
It focuses on building a small, well-defined **LLM-powered autonomous agent** to understand core concepts such as agent reasoning, tool usage, and Retrieval-Augmented Generation (RAG).

---

## Agent Definition

**Agent Name (Conceptual):** Cyber Threat Explainer Agent  

**Purpose:**  
Explain cybersecurity threats and defensive concepts using curated Cyber Threat Intelligence (CTI) documents through a RAG-based approach.

The agent is designed to analyse user queries, retrieve relevant security knowledge when required, and generate clear, structured explanations.

---

## Agent Characteristics

The prototype demonstrates agent behaviour through:  
- Multi-step reasoning  
- Intent-based routing  
- Query reformulation for improved retrieval  
- Intentional use of internal tools  

This design reflects autonomous agent principles rather than simple prompt-based interaction.

---

## High-Level Flow

1. The agent receives a user query  
2. The agent determines the intent of the query  
3. The agent decides whether external CTI knowledge is required  
4. If required:  
   - The query is reformulated  
   - Relevant CTI documents are retrieved  
   - An explanation is synthesised  
5. The agent returns a final response  

---

## Agent Flow Structure

<img width="313" height="643" alt="Prototype Data FLow drawio" src="https://github.com/user-attachments/assets/c9e328d5-0ed5-42fd-8183-b61b129c956d" />


---

## Internal Tools

**decide_need_rag(query)**  
Determines whether the query requires external CTI knowledge.

**search_cti(query)**  
Performs similarity search over CTI documents using vector embeddings and Chroma.

**synthesize_explanation(chunks, query)**  
Combines retrieved CTI information and generates a clear, grounded explanation.

---

## CTI Dataset

The CTI dataset is intentionally small to support effective experimentation.

Dataset characteristics:  
- 10–20 short documents  
- Based on authoritative cybersecurity sources  
- Focused on attack techniques, common threats, and mitigation strategies  

This scope is sufficient to demonstrate RAG functionality and evaluate retrieval quality.

---

## RAG Pipeline

- CTI documents are ingested  
- Text is chunked into manageable segments  
- Embeddings are generated  
- Embeddings are stored in Chroma  
- Relevant chunks are retrieved through similarity search  
- The LLM synthesises an explanation based on retrieved content  

---

## User Interface

The prototype includes a minimal user interface for interaction with the agent.

Features:  
- Text-based input  
- Chat-style responses  
- Streaming output  

The interface prioritises functionality and clarity over visual complexity.

---

## Extensibility

The prototype is designed as a foundation for future extension into a multi-agent system.  
Additional agents can be introduced later without changing the core flow or architecture.

---

