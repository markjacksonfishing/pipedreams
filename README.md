# PipeDreams - CSV Data Explorer

![PipeDreams Header](images/istockphoto-1502938892-612x612.jpg)

PipeDreams is a data exploration and visualization tool designed to be simple, flexible, and powerful. Upload any CSV file, perform basic ETL transformations, visualize your data, and gain insights with built-in machine learning—all from a user-friendly Streamlit interface. If no file is uploaded, a default dataset (`customers-100000.csv`) is used for demonstration.

## Features

- **CSV Upload**: Upload any CSV file for immediate analysis and visualization.
- **Default Dataset**: If no file is uploaded, the app loads a sample dataset (`customers-100000.csv`) located in the `data/` directory.
- **ETL Transformations**: Clean and transform data, remove missing values, and auto-convert data types.
- **Data Visualization**: Interactive charts (scatter, bar, line, histogram, and box plots) to gain insights from your data.
- **Clustering Analysis**: Use KMeans clustering to identify natural groupings within the data, helping to segment and classify.
- **Predictive Analysis**: A synthetic column (`Annual Purchase Amount`) is included for testing linear regression, allowing users to explore predictive analysis features.

## Getting Started

### Prerequisites

- **Python** (version 3.6 or higher)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/markjacksonfishing/pipedreams.git
   cd pipedreams
   ```

2. **Set up a virtual environment**:
   - **MacOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   - **MacOS/Linux**:
     ```bash
     source venv/bin/activate
     streamlit run app.py
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     streamlit run app.py
     ```

   The application will open in your default web browser at `http://localhost:8501`, and will look like this:
   ![PipeDreams - Enhanced Data Explorer](images/running_broswer.jpeg)

5. **Deactivate the virtual environment** (when finished):
   ```bash
   deactivate
   ```

### How to Use

1. Start the application by following the setup steps above.
2. **Upload a CSV file** using the file uploader in the app, or view the **default dataset** if no file is uploaded.
3. Explore the data with built-in ETL transformations and interactive visualizations.
4. Perform **clustering analysis** and **predictive analysis** on available data.

### Advanced Insights: Clustering and Predictive Analysis

- **Clustering Analysis**: Select features for clustering, and the app will automatically group data into clusters using KMeans. This can reveal natural groupings in the data, such as customer segments.
- **Predictive Analysis**: Select features and a target variable (e.g., the synthetic `Annual Purchase Amount`) for linear regression. The app will generate a prediction model, display a mean squared error metric, and show an interactive scatter plot comparing actual vs. predicted values.

### Default Dataset: `customers-100000.csv`

The default dataset, `customers-100000.csv`, is located in the `data/` directory. If no CSV file is uploaded, this dataset will automatically load, allowing users to test the ETL transformations, visualizations, clustering, and predictive analysis features without needing their own data file.
```
