# PipeDreams

![Pipeline Image](istockphoto-1502938892-612x612.jpg)

PipeDreams is a streamlined, containerized ETL (Extract, Transform, Load) pipeline designed to process and visualize data efficiently. Inspired by the need for simple yet powerful data workflows, this project lets users deploy a complete data pipeline in minutes, from raw data ingestion to insightful visualizations.

Whether you’re an analyst, data engineer, or developer, PipeDreams makes it easy to transform your data and gain insights without the overhead of complex setup and maintenance. With the goal of providing an intuitive, self-contained experience, this pipeline is deployable locally using Minikube, bringing everything you need right to your fingertips.

## Features

- **Automated ETL Process**: Extract, transform, and load data from a CSV file into a SQLite database, ready for exploration.
- **Interactive Data Visualization**: Powered by Streamlit, the frontend offers a clean, interactive way to explore and analyze processed data.
- **Containerized & Deployable**: Everything runs in Docker containers, making it easy to set up, deploy, and scale locally using Minikube.
- **Simple Setup**: With a single `setup.sh` script, PipeDreams handles all installations, builds, and configurations, making setup effortless.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Docker
- Minikube
- Kubernetes CLI (`kubectl`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/markjacksonfishing/pipedreams.git
   cd pipedreams
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Access the Streamlit app**: Once deployed, the Minikube service will display the URL for accessing the Streamlit application, where you can interact with your data.

## Repository Structure

```plaintext
pipedreams/
├── README.md
├── setup.sh                  # Shell script to set up the entire project
├── data/
│   └── customers.csv         # CSV file for ETL processing
├── k8s-manifests/            # Kubernetes manifests for Minikube deployment
│   ├── pvc.yaml              # PVC for database storage
│   ├── etl-deployment.yaml   # ETL job deployment
│   ├── streamlit-deployment.yaml # Streamlit app deployment
│   └── streamlit-service.yaml    # Service to expose Streamlit
├── etl/
│   ├── Dockerfile            # Dockerfile for ETL
│   └── etl_script.py         # ETL script
└── streamlit_app/
    ├── Dockerfile            # Dockerfile for Streamlit app
    └── app.py                # Streamlit application
```

## Pipeline Overview

1. **Extract**: Reads data from `customers.csv`, a sample dataset located in the `data/` directory.
2. **Transform**: Cleans and processes the data to prepare it for analysis. This includes normalizing fields, handling missing values, and formatting dates.
3. **Load**: Stores the processed data in a SQLite database, making it easily accessible to the Streamlit frontend.

## Why PipeDreams?

PipeDreams aims to simplify the data pipeline creation process. With a single command, users can go from raw data to a fully interactive dashboard without wrestling with dependencies or complex setups. This project is ideal for those who need a fast, reliable, and local data pipeline for analysis or prototyping purposes.

## Future Enhancements

- **Expanded Data Sources**: Adding support for multiple input data formats.
- **Advanced Visualization**: Implementing more sophisticated visualizations for deeper insights.
- **Cloud Deployment Options**: Extending deployment capabilities to cloud platforms.

## Contributing

Contributions are welcome! If you’d like to contribute, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
