# Agentic RAG Course Planning Assistant

This project implements a catalog-grounded course planning assistant using a Retrieval Augmented Generation (RAG) pipeline. The system answers prerequisite questions and generates semester course plans strictly based on course catalog documents.

## Features

- Prerequisite eligibility reasoning  
- Multi-hop prerequisite chain handling  
- Course plan generation  
- Clarifying questions when info missing  
- Safe abstention for unknown queries  
- Citation-grounded responses  
- Structured output format  

---

## Architecture

Pipeline:

User Query  
→ Retriever (FAISS + MiniLM)  
→ Catalog Extraction  
→ Prerequisite Reasoner (multi-hop)  
→ Course Planner  
→ Verifier  
→ Structured Response with Citations  

---

## RAG Configuration

- Embeddings: sentence-transformers/all-MiniLM-L6-v2  
- Vector Store: FAISS  
- Chunk Size: 800  
- Chunk Overlap: 100  
- Retriever: similarity search (top-k = 4)  

---

## Dataset

Synthetic academic catalog with 20+ courses including:

- core CS courses  
- AI/ML track courses  
- math prerequisites  
- multi-hop prerequisite chains  

Example:

CS101 → CS102 → CS201 → CS301 → CS401

---

## Example Queries

Prerequisite reasoning:


Can I take CS301 after CS101?


Course planning:


Completed: CS101 CS102 CS201 plan my semester


Clarifying question:


Can I take CS301?


Safe abstention:


Who teaches CS301?


---

## Setup

Install dependencies:


pip install -r requirements.txt


Build vector index:


python build_index.py


Run assistant:


python query.py


---

## Output Format

Each response includes:

- Answer / Plan  
- Why (prerequisite reasoning)  
- Citations  
- Clarifying Questions  
- Assumptions / Not in catalog  

---

## Evaluation

The evaluation set includes:

- prerequisite eligibility checks  
- multi-hop chain reasoning  
- course planning queries  
- clarification cases  
- abstention cases  

Run evaluation:


python evaluation/run_eval.py


---

## Project Structure


course_planner_rag/
│
├── data/
├── planner/
├── evaluation/
├── faiss_index/
│
├── build_index.py
├── query.py
├── requirements.txt
├── README.md
└── SOURCES.md


---

## Notes

- The system is fully catalog-grounded  
- No hallucinated prerequisites are generated  
- Planner supports recursive prerequisite chains  
- Course recommendations filtered by eligibility  