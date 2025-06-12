#!/bin/bash

build_cluster_state_image() {
    echo "Building Docker image kubegraph-cluster-state:latest..."
    cd cluster-state || exit 1
    sudo docker build --progress=plain --no-cache -t kubegraph-cluster-state:latest .
    cd .. || exit 1
}

build_api_image() {
    echo "Building Docker image kubegraph-api:latest..."
    cd api || exit 1
    sudo docker build --progress=plain --no-cache -t kubegraph-api:latest .
    cd .. || exit 1
}

run_compose() {
    echo "Starting Docker Compose with docker-compose.test.yaml..."
    sudo docker compose -f docker-compose.test.yaml up
}

build_cluster_state_image
build_api_image
run_compose
