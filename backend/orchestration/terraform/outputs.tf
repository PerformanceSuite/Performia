output "pubsub_topics" {
  value = [
    google_pubsub_topic.ingest.name,
    google_pubsub_topic.separate.name,
    google_pubsub_topic.analyze.name,
    google_pubsub_topic.package.name
  ]
}

output "pubsub_subscriptions" {
  value = [
    google_pubsub_subscription.ingest.name,
    google_pubsub_subscription.separate.name,
    google_pubsub_subscription.analyze.name,
    google_pubsub_subscription.package.name
  ]
}

output "artifact_repo" {
  value = google_artifact_registry_repository.repo.repository_id
}

output "bucket" {
  value = google_storage_bucket.artifacts.name
}
