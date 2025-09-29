locals {
  base_image_path = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}"

  cloud_run_jobs = {
    ingest = {
      image   = "${local.base_image_path}/ingest:${var.cloud_run_image_tag}"
      timeout = "900s"
      env = {
        GCS_BUCKET   = google_storage_bucket.artifacts.name
        PUBSUB_TOPIC = google_pubsub_topic.ingest.name
        PUBSUB_OUT   = google_pubsub_topic.separate.name
      }
    }

    packager = {
      image   = "${local.base_image_path}/packager:${var.cloud_run_image_tag}"
      timeout = "900s"
      env = {
        GCS_BUCKET   = google_storage_bucket.artifacts.name
        PUBSUB_TOPIC = google_pubsub_topic.package.name
      }
    }
  }
}

resource "google_service_account" "pipeline" {
  account_id   = "${var.pubsub_prefix}-runner"
  display_name = "Music AI Pipeline Runner"
}

resource "google_cloud_run_v2_job" "jobs" {
  for_each = local.cloud_run_jobs

  name     = "${var.pubsub_prefix}-${each.key}"
  location = var.region

  template {
    template {
      service_account = google_service_account.pipeline.email

      containers {
        image = each.value.image

        dynamic "env" {
          for_each = each.value.env
          content {
            name  = env.key
            value = env.value
          }
        }
      }

      timeout = each.value.timeout
    }
  }
}
