# Domain Module: AI & Machine Learning

## Trigger
Use when a task involves selecting, integrating, evaluating, or building AI/ML models, LLM applications, embeddings, RAG, fine-tuning, or model-serving pipelines.

## Workflow
1. Clarify the target task, quality criteria, latency, privacy, deployment environment, and budget.
2. Determine whether a hosted API, open model, classical ML method, or deterministic software is the right fit; do not assume an LLM is required.
3. Identify data provenance, permissions, sensitivity, retention, and evaluation splits before processing data.
4. Choose model candidates based on task performance, license, context/window limits, hardware requirements, latency, and cost.
5. For RAG, design ingestion, chunking, metadata, retrieval, reranking, citation grounding, and access filtering as separate steps.
6. For fine-tuning, establish a baseline, validate dataset rights and quality, prevent train/test leakage, and compare against the baseline.
7. Add structured outputs, timeouts, retries, rate limits, and safe fallbacks.
8. Evaluate factuality, task success, bias, privacy leakage, robustness, and cost using representative test cases.
9. Record model ID, exact version, prompt/configuration, data version, metrics, and known failure modes.

## Outputs
A reproducible model/integration recommendation, architecture, evaluation plan, and tested implementation or change proposal.

## Boundaries
Do not expose private data to unapproved providers, claim benchmark superiority without comparable measurements, or train on content without usage rights.
