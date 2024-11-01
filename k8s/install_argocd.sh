#!/bin/bash

# Set Argo CD namespace and application variables
NAMESPACE="argocd"
APP_NAME="pipedreams"
REPO_URL="https://github.com/markjacksonfishing/pipedreams.git"
REPO_PATH="k8s"  # Path within the repo where YAML files are stored

# Step 1: Install Argo CD
echo "Installing Argo CD in namespace $NAMESPACE..."
kubectl create namespace $NAMESPACE
kubectl apply -n $NAMESPACE -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Step 2: Wait for Argo CD components to be ready
echo "Waiting for Argo CD components to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/argocd-server -n $NAMESPACE

# Step 3: Set up port forwarding and add a brief delay
echo "Setting up port forwarding to access Argo CD UI on https://localhost:8080"
kubectl port-forward svc/argocd-server -n $NAMESPACE 8080:443 > /dev/null 2>&1 &
sleep 5  # Brief delay to ensure port forwarding is ready

# Step 4: Retrieve initial admin password and login to Argo CD CLI
echo "Retrieving initial Argo CD admin password..."
ARGOCD_PWD=$(kubectl get secret argocd-initial-admin-secret -n $NAMESPACE -o jsonpath="{.data.password}" | base64 -d)

echo "Logging into Argo CD with initial password..."
argocd login localhost:8080 --username admin --password "$ARGOCD_PWD" --insecure || { echo "Login failed with initial password"; exit 1; }

# Step 5: Change the Argo CD admin password and verify
NEW_PASSWORD="mynewpassword"  # Change this to a secure password
echo "Setting new Argo CD admin password..."
argocd account update-password --current-password "$ARGOCD_PWD" --new-password "$NEW_PASSWORD"

# Verify new password by logging in
echo "Verifying new password..."
if argocd login localhost:8080 --username admin --password "$NEW_PASSWORD" --insecure; then
    echo "Password updated and verified successfully."
else
    echo "Password update verification failed."
    exit 1
fi

# Step 6: Wait for Argo CD repository server to be ready
echo "Waiting for Argo CD repository server to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/argocd-repo-server -n $NAMESPACE

# Step 7: Create Argo CD Application for GitOps
echo "Creating Argo CD application for $APP_NAME from repo $REPO_URL..."
argocd app create $APP_NAME \
    --repo $REPO_URL \
    --path $REPO_PATH \
    --dest-server https://kubernetes.default.svc \
    --dest-namespace pipedreams \
    --sync-policy auto

echo "Argo CD setup complete. Access the UI at https://localhost:8080"
echo "Login with username: admin and password: $NEW_PASSWORD"
echo "To stop port forwarding, run 'kill %1'"
