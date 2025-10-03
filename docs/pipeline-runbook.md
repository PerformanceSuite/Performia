# Music AI Pipeline Runbook

## Overview
The ingest-analyze pipeline ingests a raw WAV, performs analysis stages, and writes a canonical Song Map back to GCS.
Cloud Run Jobs handle lightweight CPU workloads (ingest, packager) while GKE Autopilot jobs process GPU-intensive tasks
(separation, melody_bass, asr). Pub/Sub topics provide fan-out between stages.

## Terraform Stack
1. `terraform init`
2. `terraform plan -var="project_id=<project>" -var="bucket_name=<bucket>"`
3. `terraform apply -var="project_id=<project>" -var="cloud_run_image_tag=<tag>"`

Resources:
- Artifact Registry Docker repository
- GCS bucket with folders: `raw/`, `stems/`, `partials/`, `final/`
- Pub/Sub topics and subscriptions (`<prefix>-ingest`, `<prefix>-separate`, `<prefix>-analyze`, `<prefix>-package`)
- Cloud Run v2 jobs (`<prefix>-ingest`, `<prefix>-packager`)
- GKE Autopilot cluster (`<prefix>-autopilot`) with workload identity bindings
- Service accounts for GPU workloads with Storage/PubSub permissions

## Deployment Flow
1. Build & push containers:
   ```bash
   make build-all IMAGE_TAG=prod
   make push-all IMAGE_TAG=prod PROJECT=<project> REPO=<repo>
   ```
2. Apply Terraform with `cloud_run_image_tag=prod`.
3. Configure Kubernetes namespace and service accounts:
   ```bash
   gcloud container clusters get-credentials <prefix>-autopilot --region <region> --project <project>
   export PUBSUB_PREFIX=<prefix>
   export GCP_PROJECT=<project>
   envsubst < orchestration/kubernetes/serviceaccounts.yaml | kubectl apply -f -
   ```
4. Deploy GPU workloads (sample manifests in `orchestration/kubernetes`):
   ```bash
   export REGION=<region>
   export ARTIFACT_REPO=<repo>
   export GCS_BUCKET=<bucket>
   export IMAGE_TAG=prod
   export JOB_ID=demo
   envsubst < orchestration/kubernetes/separation-job.yaml | kubectl apply -f -
   ```
5. Trigger pipeline by publishing `ingest` job message or uploading raw audio to GCS and invoking Cloud Run job:
   ```bash
   gcloud run jobs execute <prefix>-ingest --project <project> --region <region> --args "--id=test --raw=gs://<bucket>/raw/test.wav"
   ```

## Monitoring & Troubleshooting
- **Cloud Logging**: filter on `resource.type="cloud_run_job"` or `k8s_cluster_name="<prefix>-autopilot"`.
- **Pub/Sub**: check dead-letter or unacked counts via `gcloud pubsub subscriptions describe`.
- **GCS**: ensure artifacts in `partials/` and `final/` match job IDs.
- **Terraform**: run `terraform plan` regularly to detect drift.

## Incident Response Checklist
- Identify failing stage by checking Pub/Sub backlog and job logs.
- Re-run the impacted stage manually via Cloud Run job or Kubernetes job with same `--id`.
- If outputs are corrupt, delete `partials/<id>.*` and `final/<id>.song_map.json` in GCS before reprocessing.
- Escalate to ML owners if model outputs diverge from expected schema.
