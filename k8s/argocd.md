## Argo CD Installation and Setup

For a streamlined GitOps setup, `PipeDreams` uses **Argo CD** to manage and synchronize application deployments in Kubernetes. The `install_argocd.sh` script automates the installation and configuration of Argo CD, as well as setting up `PipeDreams` as an Argo CD-managed application.

### Script Overview

The `install_argocd.sh` script performs the following steps:

1. **Installs Argo CD** in the Kubernetes cluster.
2. **Waits** for the Argo CD components to be fully ready.
3. **Sets up port forwarding** for local access to the Argo CD UI at `https://localhost:8080`.
4. **Retrieves the initial Argo CD admin password** from Kubernetes secrets, logs into Argo CD, and updates the password.
5. **Configures the Argo CD Application** for `PipeDreams`, setting it to sync automatically with the GitHub repository.

### Usage of `install_argocd.sh`

To use the script, follow these steps:

1. **Ensure Minikube is running** with `minikube start` and that `kubectl` is configured to use the Minikube context.
2. **Execute the script** in the terminal:

   ```bash
   ./install_argocd.sh
   ```

3. **Script Output**:
   - The script will install Argo CD, log in, and configure the `PipeDreams` application to sync from the GitHub repository.
   - Once complete, access Argo CD’s UI at [https://localhost:8080](https://localhost:8080), using `admin` as the username and the updated password specified in the script.

### Important Notes

- **Port Forwarding**: The script sets up port forwarding to `localhost:8080` for accessing the Argo CD UI. To stop the port forwarding, use the command:

  ```bash
  kill %1
  ```

- **Auto-Sync with GitHub**: The `PipeDreams` application is configured in Argo CD with auto-sync enabled. Any updates pushed to the repository will trigger an automatic deployment in the Kubernetes cluster.

By integrating Argo CD, this setup enables a fully automated GitOps workflow, where `PipeDreams` is continuously deployed from source code to production. This approach helps streamline operations, increase deployment speed, and maintain version control for Kubernetes resources.
