variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "artifact_repo" {
  type    = string
  default = "music-ai"
}

variable "bucket_name" {
  type    = string
  default = "music-ai-artifacts"
}

variable "pubsub_prefix" {
  type    = string
  default = "musicai"
}

variable "subscription_ack_deadline" {
  description = "Ack deadline for Pub/Sub subscriptions (seconds)."
  type        = number
  default     = 60
}

variable "subscription_retention" {
  description = "How long to retain acked messages (RFC3339 duration)."
  type        = string
  default     = "86400s"
}

variable "cloud_run_image_tag" {
  description = "Container tag to deploy for Cloud Run jobs."
  type        = string
  default     = "latest"
}
