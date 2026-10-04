# 🏛️ AutoGov AI — Your Government Services Navigator

AutoGov AI is an agentic AI assistant designed to simplify Pakistani public service applications (NADRA, Passport/DGIP, and FBR). It verifies official government policy guidelines using vector RAG search and compiles pre-filled, submission-ready PDF forms for citizens.

---

## ⚡ Key Features

- **🏛️ Multi-Department Support:** Coverage for NADRA (CNIC renewal), DGIP (Passports), and FBR (NTN registration).
- **🔍 Vector RAG Engine:** FAISS vector database + Groq (`llama-3.3-70b-versatile`) for precise, anti-hallucination policy extraction.
- **📄 Pre-Filled Official PDF Generation:** Uses ReportLab to generate official application forms with auto-formatted CNICs, standard dates, and document checklists.
- **📊 Application Readiness Gauge:** Live input auditing that guides applicants toward a 100% complete application.
- **🌐 Bilingual Interface:** Built-in English and Urdu UI support for local accessibility.

---

## 🚀 Quickstart Guide

### Clone Repository & Install Dependencies

```bash
git clone https://github.com/ariesshadow/AUTOGOV-AI.git
cd AUTOGOV-AI
pip install -r requirements.txt
