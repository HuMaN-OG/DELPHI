<div align="center">

# 🔮 DELPHI
### The Autonomous Tri-Agent Pre-Launch Product Auditor

[![Live Demo](https://img.shields.io/badge/Live%20Demo-delphi--eight.vercel.app-7C3AED?style=for-the-badge&logo=vercel&logoColor=white)](https://delphi-eight.vercel.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-VanshMiglani007%2FDELPHI-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VanshMiglani007/DELPHI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/Frontend-React%2019-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Groq LLaMA 3.1](https://img.shields.io/badge/AI%20Engine-Groq%20LLaMA--3.1-FF4B4B?style=for-the-badge&logo=openai&logoColor=white)](https://groq.com/)

<p align="center">
  <b>Three autonomous AI agents simultaneously analyze any live web product from a Technical, Human, and Business perspective — revealing the unvarnished truth before launch.</b>
</p>

[🌐 Try Live Application](https://delphi-eight.vercel.app/) • [📽️ View Pitch Presentation Deck](pitch.html) • [⚡ Report Issue](https://github.com/VanshMiglani007/DELPHI/issues)

---

</div>

## 📌 Table of Contents
- [Overview](#-overview)
- [The Tri-Agent Architecture](#-the-tri-agent-architecture)
  - [1. 🛡️ Sentinel — Technical & Infrastructure Agent](#1-️-sentinel--technical--infrastructure-agent)
  - [2. 👤 Stranger — UX & Friction Agent](#2--stranger--ux--friction-agent)
  - [3. 🔮 Oracle — Business & Positioning Agent](#3--oracle--business--positioning-agent)
- [System Architecture & Real-Time Pipeline](#-system-architecture--real-time-pipeline)
- [Scoring & Verdict Engine](#-scoring--verdict-engine)
- [Key Features & Highlights](#-key-features--highlights)
- [Tech Stack](#-tech-stack)
- [Directory Structure](#-directory-structure)
- [Getting Started & Local Setup](#-getting-started--local-setup)
  - [Prerequisites](#prerequisites)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [License](#-license)

---

## My role and demo evidence

This is a three-person hackathon project from SRM Build 7.0. My reported contributions include integration/deployment and coordinating the multi-agent analysis with the live React dashboard. These statements describe my work in a team, not independent authorship of every file.

Reviewers can open the live demo linked above and inspect the system architecture below. To strengthen the portfolio, add real screenshots showing (1) a public test URL, (2) the streaming analysis UI and (3) the resulting recommendations. Avoid testing URLs without authorization or revealing private data. Screenshots are not claimed here until actually captured.

---

## 🚀 Overview

Launching a digital product without comprehensive auditing leads to silent user churn, unhedged security vulnerabilities, and positioning failure. Most product teams audit engineering, UX design, and marketing in silos.

**DELPHI** solves this by deploying **three specialized autonomous AI agents** in parallel over high-speed WebSocket streams to inspect any web URL. Each agent conducts real-time automated deep-dives into a crucial pillar of product survival:
1. **Infrastructure & Security Resilience**
2. **First-Time User Friction & Conversion Signals**
3. **Business Positioning & Value Proposition Clarity**

As findings stream live into a cyberpunk-inspired dashboard, DELPHI computes a composite **DELPHI Score**, calculates **Launch Survival Probability**, and synthesizes an LLM-driven prioritized roadmap of fixes powered by **Groq LLaMA-3.1**.

---

## 🤖 The Tri-Agent Architecture

```
                       ┌────────────────────────────────────────┐
                       │          Target URL Submitted          │
                       └───────────────────┬────────────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        │      FastAPI WebSocket Manager      │
                        └─────────┬──────────┬──────────┬─────┘
                                  │          │          │
             ┌────────────────────┘          │          └───────────────────┐
             ▼                               ▼                              ▼
    🛡️ SENTINEL (Tech)              👤 STRANGER (UX)             🔮 ORACLE (Business)
┌─────────────────────────┐     ┌─────────────────────────┐    ┌─────────────────────────┐
│ • Autonomous Crawler    │     │ • First Impression View │    │ • Value Prop Auditor    │
│ • Security Header Scan  │     │ • Above-the-fold CTA    │    │ • Pricing Path Analysis │
│ • 500-User Stress Test  │     │ • Form Field Friction   │    │ • Social Proof Matrix   │
│ • SQLi/XSS/Fuzzing      │     │ • Trust Signal Check    │    │ • Broken Link Audit     │
│ • SSL Certificate Audit │     │ • Mobile Viewport Check │    │ • Copy Professionalism  │
└────────────┬────────────┘     └────────────┬────────────┘    └────────────┬────────────┘
             │                               │                              │
             └───────────────────┬───────────┴──────────────────────────────┘
                                 │
                                 ▼
                     ┌──────────────────────┐
                     │ Groq LLaMA-3.1 LLM   │
                     │ Verdict & Fix Engine │
                     └───────────┬──────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Composite DELPHI Score │
                    │   Survival Probability  │
                    │   Prioritized Fix Plan  │
                    └─────────────────────────┘
```

### 1. 🛡️ Sentinel — Technical & Infrastructure Agent
*Assesses system stability, security posture, and stress limits under load.*

- **Autonomous Web Crawling:** Discovers internal domain endpoints and extracts interactive form schemas.
- **Security Header Audit:** Verifies enforcement of `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security` (HSTS), `X-Content-Type-Options`, `X-XSS-Protection`, and `Referrer-Policy`.
- **Progressive Load Testing:** Spawns concurrent background threads via `ThreadPoolExecutor` simulating 10 to 500+ virtual users to determine maximum concurrency breaking points (>20% error rate).
- **Vulnerability Input Fuzzing:** Injects SQL Injection (`' OR 1=1--`), Reflected XSS (`<script>`), and Path Traversal payloads into forms to detect unhandled exceptions and security flaws.
- **SSL/TLS Validation:** Verifies active SSL encryption validity and expiration date.

### 2. 👤 Stranger — UX & Friction Agent
*Evaluates the product experience through the lens of a first-time user.*

- **First Impression & CTA Visibility:** Checks if high-intent call-to-action buttons (*"Get Started"*, *"Try Free"*, *"Sign Up"*) appear above the fold.
- **Signup Flow Friction Index:** Analyzes onboarding form length; flags forms with >5 input fields that drive user drop-off.
- **Trust Signal Matrix:** Scans DOM for testimonials, pricing tables, privacy policies, contact methods, and security badges.
- **Mobile Viewport Emulation:** Simulates iOS mobile viewports (375x812) to detect viewport scaling and layout breaks.

### 3. 🔮 Oracle — Business & Positioning Agent
*Audits market positioning, copy clarity, and conversion drivers.*

- **Value Proposition Clarity:** Scans copy for vague, hyper-generic buzzwords (*"revolutionary"*, *"next-gen"*, *"paradigm shift"*) that obscure true product utility.
- **Pricing Strategy Discovery:** Identifies clear user paths to pricing plans (`/pricing`, `/plans`).
- **Social Proof Quantification:** Evaluates metrics across user counts, press mentions, star ratings, and testimonials.
- **Action-Oriented CTA Copy:** Flags weak passive text (*"Submit"*, *"Click Here"*) in favor of high-converting action language (*"Start Free"*, *"Book Demo"*).
- **Broken Link Health Check:** Asynchronously tests extracted outbound and internal URLs for 404/500 HTTP status codes.
- **Professionalism Audit:** Scans text for excessive ALL CAPS usage and unprofessional punctuation (`!!`).

---

## 🧮 Scoring & Verdict Engine

DELPHI employs a deterministic scoring model coupled with LLM synthesis:

### Agent Score Formula
Each agent starts at **100** points, receiving severity-weighted deductions for detected issues:

$$\text{Score}_{\text{Agent}} = \max\left(0, 100 - \sum \text{Deductions}\right)$$

| Finding Severity | Penalty Points |
| :--- | :--- |
| **CRITICAL** | `-20` pts |
| **HIGH** | `-10` pts |
| **MEDIUM** | `-5` pts |
| **LOW** | `-2` pts |

### Composite DELPHI Score
$$\text{DELPHI Score} = \lfloor (0.40 \times \text{Sentinel}) + (0.30 \times \text{Stranger}) + (0.30 \times \text{Oracle}) \rfloor$$

### Survival Probability
$$\text{Survival Probability} = \max(0, \text{DELPHI Score} - 10)$$

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19 (`react`, `react-dom`)
- **Styling:** Custom CSS Design System, Glassmorphism, Theme Switcher (Dark/Light)
- **UI & Motion:** `lucide-react`, `framer-motion`, `recharts`
- **Real-Time Data:** Native WebSockets with client-side simulation fallback

### Backend
- **Framework:** FastAPI (`uvicorn`, `pydantic`)
- **Real-Time Channels:** Python `asyncio`, `WebSockets ConnectionManager`
- **Web Analysis:** `beautifulsoup4`, `requests`, `ssl`, `socket`
- **AI Engine:** Groq SDK (`llama-3.1-8b-instant` model)
- **Concurrency Execution:** `concurrent.futures.ThreadPoolExecutor`

---

## 📁 Directory Structure

```
DELPHI/
├── backend/
│   ├── agents/
│   │   ├── oracle.py           # Business & positioning agent
│   │   ├── sentinel.py         # Technical & security auditor
│   │   └── stranger.py         # UX friction & user perception auditor
│   ├── core/
│   │   ├── ollama_client.py    # Groq LLM streaming client
│   │   ├── prompts.py          # AI agent prompt templates
│   │   └── scorer.py           # DELPHI scoring & math algorithms
│   ├── main.py                 # FastAPI server & WebSocket manager
│   ├── requirements.txt        # Python backend dependencies
│   └── test_client.py          # CLI socket testing utility
├── frontend/
│   ├── public/                 # Static web assets
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── AgentPanel.jsx      # Live agent stream card
│   │   │   ├── Dashboard.jsx       # Multi-agent streaming view
│   │   │   ├── FinalVerdict.jsx    # Verdict summary & action plan
│   │   │   ├── FindingCard.jsx     # Finding severity badges
│   │   │   ├── Landing.jsx         # Hero section & URL input
│   │   │   ├── MetricsBar.jsx      # Telemetry metrics bar
│   │   │   └── ReasoningStream.jsx # Live terminal logs
│   │   ├── hooks/
│   │   │   └── useWebSocket.js # Real-time state manager
│   │   ├── testSocket.js       # Simulation mode handler
│   │   ├── App.js              # Main application root
│   │   └── index.css           # Global CSS variables & styles
│   └── package.json            # Node.js dependencies
├── pitch.html                  # Interactive Pitch Presentation Deck
├── LICENSE                     # MIT License
└── README.md                   # Project Documentation
```

---

## 💻 Getting Started & Local Setup

### Prerequisites
- **Python:** 3.10 or higher
- **Node.js:** 18.0 or higher
- **Groq API Key:** Obtain a free key from [consolegroq.com](https://console.groq.com)

### 1. Clone Repository
```bash
git clone https://github.com/VanshMiglani007/DELPHI.git
cd DELPHI
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API Key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Start FastAPI server
python main.py
```
The backend server will run on `http://localhost:8000`.

### 3. Frontend Setup
In a separate terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js packages
npm install

# Start React development server
npm start
```
The frontend application will open on `http://localhost:3000`.

---

## 🔑 Environment Variables

| Variable Name | Location | Required | Description |
| :--- | :--- | :--- | :--- |
| `GROQ_API_KEY` | `backend/.env` | Yes | Groq API Key powering LLaMA-3.1 completions and fix generation |
| `PORT` | Environment / Server | Optional | Backend port (defaults to `8000`) |

---

## 🌐 Live Deployments

- **Frontend App:** [https://delphi-eight.vercel.app/](https://delphi-eight.vercel.app/)
- **Backend API:** `https://delphi-backend.onrender.com`
- **GitHub Repository:** [https://github.com/VanshMiglani007/DELPHI](https://github.com/VanshMiglani007/DELPHI)

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

<div align="center">

---

Crafted with ⚡ by [Vansh Miglani](https://github.com/VanshMiglani007)

</div>
