locals {
  gke_namespace        = "${var.pubsub_prefix}-pipeline"
  workload_identity_ns = "${var.project_id}.svc.id.goog"
  gpu_service_accounts = {
    separation  = "${var.pubsub_prefix}-separation"
    melody_bass = "${var.pubsub_prefix}-melody"
    asr         = "${var.pubsub_prefix}-asr"
  }
}

resource "google_container_cluster" "autopilot" {
  name             = "${var.pubsub_prefix}-autopilot"
  location         = var.region
  enable_autopilot = true

  release_channel {
    channel = "REGULAR"
  }

  workload_identity_config {
    workload_pool = local.workload_identity_ns
  }

  logging_config {
    enable_components = [
      "SYSTEM_COMPONENTS",
      "WORKLOADS"
    ]
  }

  monitoring_config {
    managed_prometheus {
      enabled = true
    }
  }
}

resource "google_service_account" "gpu" {
  for_each = local.gpu_service_accounts

  account_id   = each.value
  display_name = "${title(replace(each.key, "_", " "))} runner"
}

resource "google_project_iam_member" "gpu_storage" {
  for_each = google_service_account.gpu

  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${each.value.email}"
}

resource "google_project_iam_member" "gpu_pubsub" {
  for_each = google_service_account.gpu

  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${each.value.email}"
}

resource "google_service_account_iam_binding" "workload_identity" {
  for_each = google_service_account.gpu

  service_account_id = each.value.name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${local.workload_identity_ns}[${local.gke_namespace}/${each.key}]"
  ]
}

output "gke_cluster_name" {
  value = google_container_cluster.autopilot.name
}

output "gke_workload_namespace" {
  value = local.gke_namespace
}

output "gpu_service_accounts" {
  value = { for k, sa in google_service_account.gpu : k => sa.email }
}
