# Google Cloud Setup Guide for Ingest-Analyze Pipeline

This guide walks you through provisioning Google Cloud resources to run the ingest-analyze pipeline. Replace placeholders
like `<project-id>` with your values when executing commands.

## 1. Create and Configure the Project
1. Create the project (skip if it already exists):
   ```bash
   gcloud projects create <project-id> --name="Performia Pipeline"
   ```
2. Link billing via Cloud Console → **Billing** → **Link a billing account**.
3. Set local defaults:
   ```bash
   gcloud config set project <project-id>
   gcloud config set compute/region us-central1
   ```

## 2. Enable Required APIs
```bash
gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  pubsub.googleapis.com \
  compute.googleapis.com \
  container.googleapis.com \
  iam.googleapis.com \
  cloudresourcemanager.googleapis.com
```

## 3. Prepare Artifact Registry & Storage
1. Create the Docker repository (Terraform defaults to `song-map` in `us-central1`):
   ```bash
   gcloud artifacts repositories create song-map \
     --repository-format=docker \
     --location=us-central1 \
     --description="Performia containers"
   ```
2. Optional: pre-create the bucket (Terraform can handle this):
   ```bash
   gsutil mb -l us-central1 gs://music-ai-artifacts
   ```

## 4. IAM and Credentials
### Developer Access
Grant yourself project-level roles (e.g., `roles/owner` during bootstrap or a mix of `roles/editor`,
`roles/iam.serviceAccountAdmin`, `roles/resourcemanager.projectIamAdmin`, `roles/storage.admin`, `roles/pubsub.admin`).

### Terraform Service Account (recommended)
```bash
gcloud iam service-accounts create terraform-admin --display-name="Terraform Admin"
gcloud projects add-iam-policy-binding <project-id> \
  --member="serviceAccount:terraform-admin@<project-id>.iam.gserviceaccount.com" \
  --role="roles/owner"
gcloud iam service-accounts keys create ~/.config/gcloud/terraform-admin.json \
  --iam-account terraform-admin@<project-id>.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/terraform-admin.json
```

## 5. Authenticate
- User credentials: `gcloud auth login` and `gcloud auth application-default login`
- Docker / Artifact Registry:
  ```bash
  gcloud auth configure-docker us-central1-docker.pkg.dev
  ```

## 6. Build & Push Containers
From `ingest-analyze-pipe/`:
```bash
make build-all IMAGE_TAG=dev-local
make push-all IMAGE_TAG=dev-local PROJECT=<project-id> REPO=song-map
```
Ensure Docker is running and authenticated to Artifact Registry.

## 7. Run Terraform
1. Copy `config/ingest-analyze.env.sample` to `.env` (optional) and fill in values.
2. Execute Terraform:
   ```bash
   cd ingest-analyze-pipe/orchestration/terraform
   terraform init
   terraform apply \
     -var="project_id=<project-id>" \
     -var="bucket_name=music-ai-artifacts" \
     -var="artifact_repo=song-map" \
     -var="pubsub_prefix=musicai" \
     -var="cloud_run_image_tag=dev-local"
   ```
3. Record outputs (topic names, subscriptions, Cloud Run jobs, GKE namespace/service accounts) for later use.

## 8. Deploy GPU Workloads on GKE
1. Pull cluster credentials:
   ```bash
   gcloud container clusters get-credentials musicai-autopilot \
     --region us-central1 \
     --project <project-id>
   ```
2. Apply namespace and service accounts:
   ```bash
   export PUBSUB_PREFIX=musicai
   export GCP_PROJECT=<project-id>
   envsubst < orchestration/kubernetes/serviceaccounts.yaml | kubectl apply -f -
   ```
3. Launch the sample separation job (replicate for melody/ASR when ready):
   ```bash
   export REGION=us-central1
   export ARTIFACT_REPO=song-map
   export GCS_BUCKET=music-ai-artifacts
   export IMAGE_TAG=dev-local
   export JOB_ID=demo
   envsubst < orchestration/kubernetes/separation-job.yaml | kubectl apply -f -
   ```

## 9. Smoke Checks
- **Artifacts**: `gsutil ls gs://music-ai-artifacts/final`
- **Cloud Run**: `gcloud run jobs list --region us-central1`
- **Pub/Sub**: `gcloud pubsub subscriptions list`
- **GKE**: `kubectl get pods -n musicai-pipeline`

## 10. Additional References
- Detailed operations runbook: `docs/pipeline-runbook.md`
- Environment template: `config/ingest-analyze.env.sample`
- Terraform outputs: run `terraform output` within the Terraform directory.

Keep credentials secure, rotate service account keys, and clean up resources when the environment is no longer needed.
