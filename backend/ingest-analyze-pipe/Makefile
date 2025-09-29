SHELL := /bin/bash

SERVICES := ingest separation beats_key chords structure asr melody_bass packager
PROJECT  ?= music-ai
REGION   ?= us-central1
REPO     ?= song-map
IMAGE_TAG ?= local
REGISTRY := $(REGION)-docker.pkg.dev/$(PROJECT)/$(REPO)

.PHONY: build-service push-service build-all push-all image-name run-packager

image-name := $(REGISTRY)/$(SERVICE):$(IMAGE_TAG)

check-service:
	@if [ -z "$(SERVICE)" ]; then \
		echo "SERVICE is required. Choose from: $(SERVICES)"; exit 1; \
	fi
	@if ! echo "$(SERVICES)" | tr ' ' '\n' | grep -qx "$(SERVICE)"; then \
		echo "Unknown SERVICE '$(SERVICE)'. Valid options: $(SERVICES)"; exit 1; \
	fi

build-service: check-service
	docker build \
		--file services/$(SERVICE)/Dockerfile \
		--tag $(image-name) \
		.

push-service: check-service
	docker push $(image-name)

build-all:
	@for svc in $(SERVICES); do \
		$(MAKE) build-service SERVICE=$$svc IMAGE_TAG=$(IMAGE_TAG); \
	 done

push-all:
	@for svc in $(SERVICES); do \
		$(MAKE) push-service SERVICE=$$svc IMAGE_TAG=$(IMAGE_TAG); \
	 done

run-packager:
	python services/packager/main.py --id demo --raw tmp/raw/demo.wav --out tmp/final
