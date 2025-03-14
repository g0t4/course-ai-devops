#!/bin/bash
set -e

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
  echo "Starting Minikube..."
  minikube start
fi

# Apply Kubernetes configurations
kubectl apply -f orders-deployment.yaml
kubectl apply -f orders-service.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=60s deployment/orders

# Get the URL to access the service
echo "Service URL:"
minikube service orders --url