# 🚀 A.I.R.A. — Autonomous Investment Research Agent

> **A production-grade, AI-powered backend system designed to autonomously analyze publicly traded companies and generate structured, explainable, and uncertainty-aware investment reports.**

A.I.R.A. showcases **agentic reasoning, asynchronous execution, multi-source data integration, hybrid AI (ML + LLM), and production-level observability** — reflecting real-world decision intelligence systems used in AI-first organizations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Core Components](#core-components)
- [Agentic Workflow](#agentic-workflow)
- [Features](#features)
- [Hybrid AI Strategy](#hybrid-ai-strategy)
- [Example Output](#example-output)
- [Observability](#observability-prometheus)
- [API Endpoints](#api-endpoints)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Key Design Decisions](#key-design-decisions)
- [Trade-offs & Known Limitations](#trade-offs--known-limitations)
- [What This Demonstrates](#what-this-demonstrates)
- [Author](#author)

---

## Overview

A.I.R.A. functions as an autonomous financial analyst. Given a stock ticker, it orchestrates a multi-agent pipeline to:

- Collect financial + market data
- Analyze sentiment with domain-specific ML
- Generate a reasoning-backed investment thesis
- Evaluate confidence and model uncertainty
- Reflect and self-correct outputs

All results are returned as **structured, explainable JSON** accessible via REST API.

---

## ⚙️ Tech Stack

### Backend & API
| Technology | Role |
|---|---|
| **FastAPI** | High-performance async API framework |
| **Uvicorn** | ASGI server |

### Distributed Processing
| Technology | Role |
|---|---|
| **Celery** | Asynchronous job execution + scheduled analysis |
| **Redis** | Message broker & task queue |

### Database
| Technology | Role |
|---|---|
| **SQLAlchemy** | ORM for job persistence and tracking |

### AI / ML
| Technology | Role |
|---|---|
| **FinBERT (HuggingFace Transformers)** | Domain-specific financial sentiment analysis |
| **OpenAI GPT (LLM)** | Reasoning, synthesis, and thesis generation |
| **Rule-based scoring** | Deterministic confidence and signal computation |

### Agent Orchestration
| Technology | Role |
|---|---|
| **Custom MCP (Model Context Protocol)** | Tool abstraction and routing layer |

### Monitoring & Observability
| Technology | Role |
|---|---|
| **Prometheus** | Metrics collection (latency, requests, errors) |

### Frontend (Optional)
| Technology | Role |
|---|---|
| **Streamlit** | Interactive analytics dashboard |

---

## 🏛️ System Architecture

```
Client (API / Streamlit)
        ↓
FastAPI Backend (API Layer)
        ↓
Celery Worker (Async Execution)
        ↓
Analysis Service
        ↓
Planner → Researcher → Synthesizer → Reflector
        ↓
MCP Layer (Tool Router & Registry)
        ↓
External Data Sources (Finance / News / SEC)
```

---

## 🧩 Core Components

### 1. API Layer (FastAPI)
- Accepts analysis requests
- Provides job status & result retrieval
- Exposes portfolio comparison endpoints
- Integrates Prometheus metrics (`/metrics`)

### 2. Asynchronous Execution (Celery + Redis)
- Handles long-running analysis tasks
- Supports retries, backoff, and fault tolerance
- Ensures non-blocking API performance
- Runs scheduled proactive analysis via **Celery Beat**

### 3. Agentic Pipeline

| Agent | Responsibility |
|---|---|
| **Planner** | Decomposes the problem and defines required data |
| **Researcher** | Retrieves structured + unstructured data via MCP |
| **Synthesizer** | Generates signal, confidence, uncertainty, and reasoning |
| **Reflector** | Evaluates output quality and adjusts confidence |

### 4. MCP (Model Context Protocol)

A modular abstraction layer for tool execution:

```
Researcher → MCP Client → Tool Router → Tool Registry → APIs
```

**Benefits:**
- Decouples agents from external APIs
- Enables plug-and-play tools
- Centralizes retries, logging, and monitoring
- Improves system extensibility

---

## 🔄 Agentic Workflow

A.I.R.A. operates as a **multi-step autonomous reasoning system**:

### 1. Planning
- Determines required data sources
- Defines execution strategy

### 2. Research
Fetches:
- Financial metrics
- Market news
- SEC filings

Applies **FinBERT** for domain-accurate sentiment scoring

### 3. Synthesis
Combines structured + unstructured inputs and produces:
- **Signal** → Bullish / Bearish / Neutral
- **Confidence Score** + **Uncertainty Score**
- **Data Quality Score**
- **Investment Thesis** (LLM-generated)

### 4. Reflection
- Multi-factor evaluation of data completeness and signal strength
- Dynamically adjusts confidence based on quality signals
- Appends transparency and reasoning notes

---

## ✨ Features

### ✅ Uncertainty Modeling
Confidence is paired with an explicit uncertainty score, giving consumers a full picture of signal reliability:
```json
"confidence": 0.42,
"uncertainty": 0.58
```

### ✅ Data Quality Scoring
Each report includes a composite data quality score based on:
- News article volume
- Financial metric availability
- SEC filing presence

### ✅ Reflection System
The Reflector evaluates four dimensions before finalizing output:
- Data completeness
- Sentiment signal strength
- Valuation risk
- Source coverage

### ✅ TTL-Based Caching
Avoids redundant analysis for recently processed tickers, reducing latency and external API cost.

### ✅ Proactive Scheduled Analysis
Celery Beat triggers daily background analysis jobs, enabling continuous market monitoring without manual requests.

### ✅ Resilient Failure Handling
- Per-source API fallbacks
- Retry mechanisms with exponential backoff
- Partial-data resilience — the pipeline continues even when one source is unavailable

---

## 🧬 Hybrid AI Strategy

A.I.R.A. combines **deterministic logic + ML + LLM**:

| Layer | Role |
|---|---|
| **FinBERT** | Extracts structured sentiment from financial news |
| **Rule-based logic** | Computes signals, confidence, and uncertainty |
| **LLM (GPT)** | Generates human-readable reasoning and thesis |

**Why this matters:**
- Reliable, auditable signal extraction
- Human-like reasoning without hallucinated numbers
- Fully explainable decisions at every layer

---

## 📊 Example Output

```json
{
  "company": "Apple Inc.",
  "ticker": "AAPL",
  "signal": "Bullish",
  "confidence": 0.42,
  "uncertainty": 0.58,
  "data_quality": 0.7,
  "insights": [
    "P/E Ratio: 33",
    "Revenue Growth: 0.12",
    "Sentiment Score: 0.3"
  ],
  "sources": ["Yahoo Finance", "NewsAPI", "SEC Filings"],
  "reflection_notes": [
    "Moderate confidence due to limited sentiment coverage"
  ]
}
```

---

## 📈 Observability (Prometheus)

A.I.R.A. exposes real-time metrics:

| Metric | Description |
|---|---|
| `aira_requests_total` | API usage per endpoint |
| `aira_request_latency_seconds` | Request latency histogram |
| `aira_errors_total` | Error tracking |
| `aira_jobs_completed_total` | Completed async jobs |

**Access metrics:**
```
http://127.0.0.1:8000/metrics
```

---

## 🛸 API Endpoints

| Endpoint | Description |
|---|---|
| `POST /analyze` | Submit analysis job |
| `GET /status/{job_id}` | Check job status |
| `GET /result/{job_id}` | Retrieve results |
| `POST /portfolio` | Compare stocks |
| `GET /metrics` | Prometheus metrics |

**Interactive API Docs:**
```
http://127.0.0.1:8000/docs
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```env
OPENAI_API_KEY=your_api_key
```

### 3. Start Redis

```bash
docker run -p 6379:6379 redis
```

### 4. Run backend

```bash
uvicorn app.main:app --reload
```

### 5. Start Celery worker

```bash
celery -A app.core.celery_app.celery worker --pool=solo --loglevel=info
```

### 6. Start Celery Beat (scheduler)

```bash
celery -A app.core.celery_app.celery beat --loglevel=info
```

### 7. Access API

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing

Run all tests:

```bash
pytest -v
```

**Coverage includes:**
- Agent pipeline
- API endpoints
- MCP layer
- Portfolio logic
- Full system integration

---

## 🎯 Key Design Decisions

### ✅ Multi-Agent Architecture
Each agent has a single, well-defined responsibility — improving modularity, traceability, and reasoning clarity.

### ✅ MCP Abstraction Layer
Agents are fully decoupled from external tools, making the system extensible without touching core logic.

### ✅ Async-first Design
Celery + Redis keep the API non-blocking under load, with built-in retry and fault-tolerance.

### ✅ Explainability-first Outputs
Every result includes signal, confidence, uncertainty, data quality, and reasoning notes — nothing is a black box.

### ✅ Observability Built-in
Prometheus metrics are embedded from day one, not bolted on after.

---

## ⚖️ Trade-offs & Known Limitations


### Trade-offs

**1. Simplicity vs. Accuracy**
- Heuristic + rule-based scoring is fast, transparent, and fully explainable
- Accuracy improves with domain-specific ML calibration over time

**2. Latency vs. Depth**
- Lightweight analysis keeps response times low and resource costs minimal
- Deeper contextual NLP is a natural next layer for richer signal extraction

**3. Deterministic Confidence**
- Rule-derived confidence is consistent, auditable, and free of hallucination
- Adaptive calibration via trained ML models is a planned enhancement

**4. MCP Abstraction**
- Adds an intentional indirection layer between agents and external tools
- Pays off immediately in modularity, testability, and long-term scalability

### Known Limitations

- **Snapshot-based analysis** — no live data streaming; results reflect point-in-time market state.
- **No long-term memory** — the system does not persist or track historical trends across runs.

---

## 🧠 What This Demonstrates

- Agentic system design with multi-step autonomous reasoning
- Backend architecture at scale with async distributed processing
- Hybrid AI integration (ML + LLM + deterministic logic)
- Uncertainty-aware, explainable AI outputs
- Production-level observability and failure resilience

---

## 👤 Author

**Andrew Adel Labib**
- 🎯 Senior AI/ML Engineer
- 📧 [andrewadellabib77@gmail.com](mailto:andrewadellabib77@gmail.com)
- 🔗 [linkedin.com/in/andrew-adel-b865b1244](https://www.linkedin.com/in/andrew-adel-b865b1244)

---
