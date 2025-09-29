# Music-AI (Ground-Up Song Map Pipeline)

This starter bundle sets up an end-to-end, **from-audio** extraction pipeline that outputs a canonical **Song Map**:
tempo/beat/downbeat, meter, key, chords, sections, lyrics, (optional) melody & bass — without third-party music catalogs.

## Sprint 1: Local Foundations
Follow these steps to get a reproducible local environment, stage demo audio, and produce a Song Map artifact.

### 1. Bootstrap the Python toolchain
```bash
cd ingest-analyze-pipe
./scripts/bootstrap_env.sh              # creates .venv and installs packager deps
source .venv/bin/activate
```
> Set `PYTHON_BIN=/path/to/python3` when the default interpreter is not desired. The
> script warns if `ffmpeg` is missing so you can install it via Homebrew or APT.

### 2. Generate or drop in demo audio
```bash
./scripts/generate_demo_wav.py          # writes tmp/raw/demo.wav (440Hz sine)
# or place your own file at tmp/raw/<name>.wav
```

### 3. Run the packager smoke test
```bash
PYTHONPATH=. python -m services.packager.main \
  --id local_test \
  --raw tmp/raw/demo.wav \
  --out tmp/final
cat tmp/final/local_test.song_map.json | jq .
```
The command emits a minimal Song Map and merges any partials located under `tmp/partials/`.

### 4. Validate with the unit test
```bash
PYTHONPATH=. pytest -q tests/unit/services/test_packager.py
```
The test executes the CLI end-to-end, validates the output against `schemas/song_map.schema.json`, and ensures the generated JSON contains the expected keys.

## Sprint 2: Core Analysis Services
Local stubs now populate every partial needed for the Song Map. Use the orchestrator to chain the services.

### 1. Run the sequential pipeline
```bash
./scripts/run_pipeline.py --id demo --raw tmp/raw/demo.wav --clean
```
> Override `--partials`, `--final`, or `--stems` to stage outputs elsewhere. The script wires
> ingest → separation → beats_key → chords → structure → asr → melody_bass → packager and prints the final artifact path.

### 2. Inspect artifacts
```bash
ls tmp/partials | grep demo
jq . tmp/final/demo.song_map.json
```
Each service drops a JSON shard named `<job>.<stage>.json`; the packager merges them into the canonical schema.

### 3. Run the enhanced test suite
```bash
PYTHONPATH=. pytest -q tests/unit/services
```
`test_pipeline.py` executes the new orchestration script end-to-end and asserts the Song Map contains beats, chords, sections, lyrics, and performance tracks.

## Sprint 3: Cloud Containerization
Build OCI images for each service and stage them in Artifact Registry ahead of Terraform deployment.

### 1. Build a single service image
```bash
make build-service SERVICE=ingest IMAGE_TAG=dev-local
```
Override registry settings by exporting `PROJECT`, `REGION`, or `REPO`. The default image path resolves to
`${REGION}-docker.pkg.dev/${PROJECT}/${REPO}/${SERVICE}:${IMAGE_TAG}` and uses the repository root as the build context.

### 2. Push to Artifact Registry
```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
make push-service SERVICE=ingest IMAGE_TAG=dev-local PROJECT=my-project REPO=song-map
```
Use `make build-all` / `make push-all` to iterate across every service. All Dockerfiles install pinned dependencies and
run `python -m services.<service>.main` as the entry point, so the same image works for Cloud Run Jobs or batch workloads.

GitHub Actions (`.github/workflows/ingest-pipeline.yml`) lint the Python layer via `pytest` and perform a Docker smoke
build on every push touching the pipeline or tests, giving early feedback before pushing to Artifact Registry.

### 3. Provision cloud infrastructure
```bash
cd orchestration/terraform
terraform init
terraform apply \\
  -var="project_id=<gcp-project>" \\
  -var="bucket_name=<gcs-bucket>" \\
  -var="cloud_run_image_tag=dev-local"
```
The Terraform stack creates an Artifact Registry repo, the `raw/`, `stems/`, `partials/`, and `final/` GCS prefixes,
Pub/Sub topics & subscriptions for each pipeline stage, a runner service account, and Cloud Run Jobs for `ingest`
and `packager`. Adjust `subscription_ack_deadline` or `subscription_retention` variables to tune Pub/Sub behaviour
before deploying additional services.

> See `docs/pipeline-runbook.md` for the full deployment & troubleshooting playbook, and populate
> `config/ingest-analyze.env.sample` for shared environment variables referenced by services and Terraform.

### 4. Deploy GPU workloads to GKE
```bash
export PUBSUB_PREFIX=musicai
export GCP_PROJECT=my-project
export REGION=us-central1
export ARTIFACT_REPO=song-map
export GCS_BUCKET=music-ai-artifacts
export IMAGE_TAG=dev-local
export JOB_ID=demo
envsubst < orchestration/kubernetes/serviceaccounts.yaml | kubectl apply -f -
envsubst < orchestration/kubernetes/separation-job.yaml | kubectl apply -f -
```
The manifests under `orchestration/kubernetes/` rely on Workload Identity bindings created by Terraform and show how to
launch the separation stage as a batch job. Replicate the pattern for melody/ASR when their containers are ready.

## Cloud Architecture (GCP)
- **GCS** buckets: `raw/`, `stems/`, `partials/`, `final/`
- **Pub/Sub**: topics: `ingest`, `separate`, `analyze`, `package`
- **Compute**:
  - Cloud Run Jobs (light CPU jobs: ingest, package, API)
  - GKE Autopilot (GPU) for heavy jobs (separation, ASR, polyphonic transcription)
- **State/Index**: Cloud SQL (Postgres) or Firestore; **BigQuery** for analytics
- **Registry**: Artifact Registry for container images
- **Observability**: Cloud Logging, Error Reporting

## Services
- `ingest`: URL → WAV (ffmpeg), upload to GCS
- `separation`: Demucs/MDX → stems
- `beats_key`: tempo, beats, downbeats, key
- `chords`: chroma features + NN/CRF smoothing
- `structure`: sections
- `asr`: Whisper (word timestamps) on vocals stem
- `melody_bass`: CREPE / Onsets&Frames / MT3
- `packager`: merges partials → **Song Map JSON**, **MIDI**, **LRC**

## Output Artifacts
- Canonical JSON schema: `schemas/song_map.schema.json`
- Example: `examples/example_song_map.json`
- REST API spec: `api/openapi.yaml`

> This is a scaffold with working stubs and placeholders so you can iterate inside your IDE.
