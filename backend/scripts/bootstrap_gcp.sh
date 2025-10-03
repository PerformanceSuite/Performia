#!/usr/bin/env bash
set -euo pipefail

# Bootstrap GCP infra with Terraform (requires gcloud auth)
cd orchestration/terraform
terraform init
terraform apply -auto-approve
