# Kubernetes Deployment Guide for PipeDreams

This document provides a step-by-step guide to deploying the `PipeDreams` application on a Kubernetes cluster using Minikube, explaining each YAML file's purpose, and detailing the commands to apply the configurations.

## Requirements

To use these YAML files for deploying `PipeDreams`, the following requirements are necessary:

- **Kubernetes Cluster**: A Kubernetes cluster is required to deploy these resources. This guide assumes you’re using Minikube, a local Kubernetes cluster tool.
- **kubectl**: Ensure `kubectl` is installed and configured to interact with your Minikube cluster.
- **Minikube**: Start Minikube by running `minikube start`.

## YAML File Overview

### 1. `pipedreams-namespace.yaml`

Defines a dedicated namespace for the `PipeDreams` application within the Kubernetes cluster. Namespaces provide isolation for resources, making it easier to manage multiple applications.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pipedreams
```

### 2. `pipedreams-deployment.yaml`

Creates a `Deployment` resource for the `PipeDreams` application, managing the following aspects:

- **Replicas**: Runs 2 replicas of the application for high availability.
- **Containers**: Specifies the container image and exposes the application on port `8501`.
- **Resource Limits**: Sets resource requests and limits to manage CPU and memory allocation efficiently.
- **Probes**: Configures `liveness` and `readiness` probes to monitor application health and readiness.
- **Security Context**: Runs the container as a non-root user for better security.
- **Pod Anti-Affinity**: Ensures pods are not scheduled on the same node, improving resilience.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pipedreams-deployment
  labels:
    app: pipedreams
spec:
  replicas: 2  # Initial replica count for high availability
  selector:
    matchLabels:
      app: pipedreams
  template:
    metadata:
      labels:
        app: pipedreams
    spec:
      containers:
      - name: pipedreams-container
        image: anuclei/pipedreams:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
      terminationGracePeriodSeconds: 30
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: pipedreams
            topologyKey: "kubernetes.io/hostname"
```

### 3. `pipedreams-hpa.yaml`

Defines a `HorizontalPodAutoscaler` (HPA) that scales the number of `PipeDreams` pods based on CPU utilization, providing flexibility to handle increased load.

- **Target Deployment**: References the `pipedreams-deployment` to scale it.
- **Min and Max Replicas**: Maintains between 2 to 5 replicas based on demand.
- **CPU Utilization Target**: Scales the application if average CPU usage exceeds 70%.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pipedreams-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pipedreams-deployment
  minReplicas: 2
  maxReplicas: 5  # Adjust based on the expected load
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Target average CPU utilization for scaling
```

### 4. `pipedreams-service.yaml`

Creates a `LoadBalancer` service to expose the `PipeDreams` application externally. This allows the application to be accessible from outside the cluster.

- **Type**: Configured as `LoadBalancer`, which Minikube can expose to the host.
- **Ports**: Routes external traffic from port `80` to the application on port `8501`.
- **Annotations**: Includes Prometheus scrape annotations for monitoring purposes.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pipedreams-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8501"
spec:
  type: LoadBalancer
  selector:
    app: pipedreams
  ports:
  - protocol: TCP
    port: 80           # Exposed port on Minikube
    targetPort: 8501   # Container's port
```

## Steps to Apply the YAML Files

1. **Create the Namespace**: Start by creating the namespace to ensure all resources are deployed within it.

   ```bash
   kubectl apply -f k8s/pipedreams-namespace.yaml
   ```

2. **Deploy the Application**: Apply the `Deployment` configuration to create the `PipeDreams` pods.

   ```bash
   kubectl apply -f k8s/pipedreams-deployment.yaml -n pipedreams
   ```

3. **Create the Service**: Set up the `Service` to expose the application.

   ```bash
   kubectl apply -f k8s/pipedreams-service.yaml -n pipedreams
   ```

4. **Configure Autoscaling**: Apply the HPA to enable dynamic scaling of the application.

   ```bash
   kubectl apply -f k8s/pipedreams-hpa.yaml -n pipedreams
   ```

5. **Access the Application**: Since Minikube does not natively support `LoadBalancer`, use `kubectl port-forward` to access the application locally.

   ```bash
   kubectl port-forward svc/pipedreams-service 8501:80 -n pipedreams
   ```

   After running this command, you can access `PipeDreams` by going to `http://localhost:8501` in your browser.

## Additional Notes

- **Autoscaling**: The Horizontal Pod Autoscaler will monitor CPU usage and scale the deployment based on the configured thresholds. Adjust `minReplicas`, `maxReplicas`, and `averageUtilization` in `pipedreams-hpa.yaml` based on expected load.
- **Monitoring**: If Prometheus is available, it can scrape metrics from this setup using the annotations in the `Service`.
- **Pod Anti-Affinity**: The deployment configuration includes anti-affinity settings to ensure pods are spread across nodes, improving resilience.

This configuration provides am awesome deployment setup for the `PipeDreams` application with considerations for high availability, scalability, and security.
