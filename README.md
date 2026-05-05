# 🚀 A.I.R.A. — Autonomous Investment Research Agent

> **A production-grade, AI-powered backend system designed to autonomously analyze publicly traded companies and generate structured, explainable, and data-driven investment reports.**

A.I.R.A. showcases **agentic reasoning, asynchronous execution, multi-source data integration, and hybrid AI (ML + LLM)** — mirroring real-world decision intelligence systems used in AI-first organizations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Core Components](#core-components)
- [Agentic Workflow](#agentic-workflow)
- [Hybrid AI Strategy](#hybrid-ai-strategy)
- [Example Output](#example-output)
- [Observability](#observability-prometheus)
- [API Endpoints](#api-endpoints)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Key Design Decisions](#key-design-decisions)
- [What This Demonstrates](#what-this-demonstrates)
- [Author](#author)

---

## Overview

A.I.R.A. is built to function as an intelligent investment analyst. Given a stock ticker, the system autonomously orchestrates a multi-agent pipeline to collect financial data, apply sentiment analysis, generate a reasoning-backed investment thesis, and reflect on output quality — all delivered as a structured JSON report accessible via REST API.

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
| **Celery** | Asynchronous job execution |
| **Redis** | Message broker & task queue |

### Database
| Technology | Role |
|---|---|
| **SQLAlchemy** | ORM for job persistence and tracking |

### AI / ML
| Technology | Role |
|---|---|
| **FinBERT (HuggingFace Transformers)** | Domain-specific sentiment analysis |
| **OpenAI GPT (LLM)** | Reasoning, synthesis, and thesis generation |

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

### 3. Agentic Pipeline

| Agent | Responsibility |
|---|---|
| **Planner** | Decomposes the problem and defines required data |
| **Researcher** | Retrieves structured + unstructured data via MCP |
| **Synthesizer** | Generates signal, confidence, and reasoning |
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

Applies **FinBERT** for sentiment scoring

### 3. Synthesis
Combines structured + unstructured inputs and produces:
- **Signal** → Bullish / Bearish / Neutral
- **Confidence Score**
- **Investment Thesis** (LLM-generated)

### 4. Reflection
- Evaluates data completeness and signal strength
- Adjusts confidence dynamically
- Adds transparency notes

---

## 🤖 Hybrid AI Strategy

A.I.R.A. combines **deterministic logic + ML + LLM**:

| Layer | Role |
|---|---|
| **FinBERT** | Extracts structured sentiment from news |
| **Rule-based logic** | Computes signals and confidence |
| **LLM (GPT)** | Generates reasoning and thesis |

**Why this matters:**
- Reliable signal extraction
- Human-like reasoning
- Explainable decisions

---

## 📊 Example Output

```json
{
  "company": "Apple Inc.",
  "ticker": "AAPL",
  "thesis": "Apple demonstrates strong fundamentals supported by positive sentiment and consistent revenue growth",
  "signal": "Bullish",
  "confidence": 0.42,
  "insights": [
    "P/E Ratio: 33.5",
    "Revenue Growth: 0.16",
    "Sentiment Score: 0.3"
  ],
  "sources": ["Yahoo Finance", "NewsAPI", "SEC Filings"],
  "reasoning": {
    "sentiment": 0.3,
    "growth": 0.16,
    "valuation": 33.5
  },
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

### 6. Access API

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
Improves modularity, traceability, and reasoning clarity

### ✅ MCP Abstraction Layer
Decouples system from external tools

### ✅ Async-first Design
Ensures scalability and responsiveness

### ✅ Explainability-first Outputs
Every result includes reasoning and confidence

### ✅ Observability Built-in
Prometheus metrics for real-time monitoring

---

## 🧠 What This Demonstrates

- Agentic system design
- Backend architecture at scale
- Hybrid AI integration (ML + LLM)
- Async distributed processing
- Production-level observability

---

## 👤 Author

**Andrew Adel Labib**
- 🎯 Senior AI/ML Engineer
- 📧 [andrewadellabib77@gmail.com](mailto:andrewadellabib77@gmail.com)
- 🔗 [linkedin.com/in/andrew-adel-b865b1244](https://www.linkedin.com/in/andrew-adel-b865b1244)

---