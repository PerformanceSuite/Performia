# Configuration

Environment variables commonly used across services:

- `GCP_PROJECT` — GCP project ID
- `GCS_BUCKET` — main bucket for artifacts (expects folders: raw/, stems/, partials/, final/)
- `PUBSUB_PREFIX` — prefix for Pub/Sub topics (defaults: ingest, separate, analyze, package)
- `AR_REPO` — Artifact Registry repo name
- `REGION` — region for Cloud Run / Artifact Registry (e.g., us-central1)
- `DB_URL` — optional Postgres/Firestore config if used for job state

Each service reads these from environment or `.env` file (see sample `.env.example`).