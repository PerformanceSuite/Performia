locals {
  subscriptions = {
    ingest   = "${var.pubsub_prefix}-ingest-worker"
    separate = "${var.pubsub_prefix}-separate-worker"
    analyze  = "${var.pubsub_prefix}-analyze-worker"
    package  = "${var.pubsub_prefix}-package-worker"
  }
}

resource "google_pubsub_topic" "ingest" {
  name = "${var.pubsub_prefix}-ingest"
}

resource "google_pubsub_topic" "separate" {
  name = "${var.pubsub_prefix}-separate"
}

resource "google_pubsub_topic" "analyze" {
  name = "${var.pubsub_prefix}-analyze"
}

resource "google_pubsub_topic" "package" {
  name = "${var.pubsub_prefix}-package"
}

resource "google_pubsub_subscription" "ingest" {
  name  = local.subscriptions.ingest
  topic = google_pubsub_topic.ingest.name

  ack_deadline_seconds       = var.subscription_ack_deadline
  message_retention_duration = var.subscription_retention
  retain_acked_messages      = true

  expiration_policy {
    ttl = ""
  }
}

resource "google_pubsub_subscription" "separate" {
  name  = local.subscriptions.separate
  topic = google_pubsub_topic.separate.name

  ack_deadline_seconds       = var.subscription_ack_deadline
  message_retention_duration = var.subscription_retention
  retain_acked_messages      = true

  expiration_policy {
    ttl = ""
  }
}

resource "google_pubsub_subscription" "analyze" {
  name  = local.subscriptions.analyze
  topic = google_pubsub_topic.analyze.name

  ack_deadline_seconds       = var.subscription_ack_deadline
  message_retention_duration = var.subscription_retention
  retain_acked_messages      = true

  expiration_policy {
    ttl = ""
  }
}

resource "google_pubsub_subscription" "package" {
  name  = local.subscriptions.package
  topic = google_pubsub_topic.package.name

  ack_deadline_seconds       = var.subscription_ack_deadline
  message_retention_duration = var.subscription_retention
  retain_acked_messages      = true

  expiration_policy {
    ttl = ""
  }
}
