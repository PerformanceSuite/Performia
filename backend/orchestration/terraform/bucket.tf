resource "google_storage_bucket" "artifacts" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 30
      matches_prefix = [
        "tmp/"
      ]
    }
  }
}

resource "google_storage_bucket_object" "folder_placeholders" {
  for_each = toset([
    "raw/",
    "stems/",
    "partials/",
    "final/"
  ])

  name    = each.value
  bucket  = google_storage_bucket.artifacts.name
  content = ""
}
