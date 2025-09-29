resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.artifact_repo
  description   = "Music-AI containers"
  format        = "DOCKER"
}
