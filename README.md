Resume–JD Evaluation Agent (LangGraph)

Overview

This project is an agentic hiring-intelligence system that evaluates a candidate’s resume against a given Job Description (JD) using multi-stage reasoning and self-evaluation.

Instead of producing a shallow keyword match or a single fit score, the system performs a structured professional review, identifying strengths, critical gaps, seniority alignment, and actionable recommendations — similar to how a hiring manager or senior engineer would assess a candidate.

The core logic is built using LangGraph, enabling explicit state management, staged reasoning, and evaluation-driven refinement.

Problem Statement

Most resume screening tools suffer from one or more of the following issues:
	•	Over-reliance on keyword matching
	•	Lack of seniority or ownership signal detection
	•	No explanation for why a candidate is rejected
	•	No actionable guidance for improvement

This project aims to solve that by answering:
	•	What does the JD actually require?
	•	What does the candidate really demonstrate?
	•	Where are the critical vs trainable gaps?
	•	Is the candidate ready for the specified role level?

System Design

The system is implemented as a multi-node LangGraph workflow:

1. Resume & JD Understanding
	•	Interprets the job description requirements
	•	Extracts explicit and implied candidate skills
	•	Identifies resume focus areas (e.g., ML, MLOps, analytics)
	•	Infers expected seniority level from the JD

2. Strict Evaluation Node
	•	Evaluates the resume as a hiring decision, not academically
	•	Separates mandatory, core, and nice-to-have skills
	•	Detects seniority signals such as ownership, deployment, and scale
	•	Determines overall role fit (Strong / Partial / Weak)

3. Self-Evaluation & Optimization
	•	Rechecks the evaluation for clarity and consistency
	•	Improves tone, structure, and decisiveness
	•	Ranks skill gaps by severity (Critical / Moderate / Low)
	•	Produces a final, human-readable hiring assessment

This staged reasoning ensures the final output is deliberate, explainable, and reliable, not a single LLM response.

Output Example

The final output includes:
	•	JD core requirements summary
	•	Candidate strengths
	•	Seniority signals (or lack thereof)
	•	Ranked skill gaps with severity
	•	Fit assessment and red flags (if any)
	•	Separate strength and role-fit scores
	•	Clear recommendations for improvement

The language is intentionally professional and mirrors real internal hiring feedback.

Why LangGraph?

LangGraph was chosen because:
	•	Resume evaluation requires multiple dependent reasoning steps
	•	Each stage benefits from structured state rather than hidden prompts
	•	Evaluation and refinement loops improve output reliability
	•	Control flow is conditional, not linear

A single LLM call or simple chain would not provide the same level of transparency or decision quality.

User Interface

A lightweight Streamlit UI is included to demonstrate the system interactively.

The UI is intentionally minimal and serves only as a visualization layer.
All core intelligence and reasoning reside in the LangGraph workflow.

Scope & Limitations
	•	The system operates on text input (resume and JD content).
	•	PDF parsing and file ingestion are intentionally out of scope.
	•	Seniority and experience are inferred heuristically and may vary with resume quality.
	•	The system provides decision support, not automated hiring decisions.

Tech Stack
	•	Python
	•	LangGraph
	•	LangChain
	•	Groq LLM (ChatGroq)
	•	Streamlit

Use Case Fit

This project demonstrates skills relevant to:
	•	Applied AI Engineer
	•	AI Engineer
	•	ML Engineer (Applied / Platform-focused)
	•	AI Product Engineer
