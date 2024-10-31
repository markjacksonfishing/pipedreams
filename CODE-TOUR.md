# CODETOUR.md

Welcome to the technical walkthrough of PipeDreams, a data exploration tool built on Streamlit that offers everything from CSV uploads and ETL transformations to data visualization and machine learning insights. Let’s go over the code step-by-step to understand what each part does and how it contributes to the functionality of this app.

## Imports and Setup

The app starts by importing the libraries we need, which include `streamlit` for the UI, `pandas` for data manipulation, and `plotly.express` for visualization. We’re also using `sklearn` for clustering (KMeans) and regression, along with other helpers like `LabelEncoder` and `StandardScaler`. `numpy` helps generate random data for testing.

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
```

## Setting the Title and App Description

The app’s header uses Streamlit’s `st.title` and `st.write` methods to display a title and description right at the top. This gives users a quick idea of the app’s purpose: uploading a CSV file, visualizing data, and diving into ETL and machine learning.

```python
st.title("PipeDreams - Enhanced Data Explorer")
st.write("Upload a CSV file to analyze, visualize, and extract deeper insights from your data using ETL and machine learning.")
```

## Loading Data

The app is set up to either use an uploaded CSV file or load a default dataset. If the user doesn’t upload a file, we load `customers-100000.csv` from the `data` directory as a sample. This provides a consistent experience for anyone exploring the app without their own data file.

```python
sample_data_path = "data/customers-100000.csv"
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("## Uploaded Data")
else:
    st.write("No file uploaded. Displaying sample data.")
    data = pd.read_csv(sample_data_path)
    st.write("## Sample Data")
st.write(data.head())
```

## Basic ETL Transformations

First, we drop any rows with missing values to keep the data clean, especially for machine learning. Then, we check if the column `Subscription Date` exists and convert it to datetime format. After that, we add a calculated column, `Years Since Subscription`, which tells us how long it’s been since each subscription. This can be helpful in clustering or predictive analysis.

```python
clean_data = data.dropna()
st.write("### Cleaned Data (no missing values)")
st.write(clean_data.head())

if 'Subscription Date' in clean_data.columns:
    clean_data['Subscription Date'] = pd.to_datetime(clean_data['Subscription Date'], errors='coerce')
    clean_data['Years Since Subscription'] = (pd.to_datetime("today") - clean_data['Subscription Date']).dt.days / 365
    st.write("### Added 'Years Since Subscription' Feature")
    st.write(clean_data[['Subscription Date', 'Years Since Subscription']].head())
```

## Encoding Categorical Data

Many machine learning algorithms can’t work directly with categorical data, so we encode categorical columns as integers using `LabelEncoder`. This allows us to use them later for clustering or predictions. Columns like `Email` and `Website` are excluded because they’re not particularly useful in numerical form.

```python
label_encoders = {}
for column in clean_data.select_dtypes(include=['object']).columns:
    if column != 'Subscription Date' and column != 'Email' and column != 'Website':
        le = LabelEncoder()
        clean_data[column] = le.fit_transform(clean_data[column])
        label_encoders[column] = le
st.write("### Categorical Columns Encoded")
st.write(clean_data.head())
```

## Generating a Synthetic Target Variable

To demonstrate predictive analysis, we create a synthetic column, `Annual Purchase Amount`, with random values. This column serves as a target variable for the regression model. By setting a random seed, we ensure reproducibility.

```python
np.random.seed(42)
clean_data['Annual Purchase Amount'] = np.random.normal(loc=5000, scale=2000, size=len(clean_data)).clip(min=0)
```

## Data Visualization

The app’s data visualization section lets users choose from five chart types (scatter plot, bar chart, line chart, histogram, and box plot). Users can select which columns to display along the X and Y axes. Only numeric columns are presented as options to prevent errors with incompatible data types.

```python
viz_type = st.selectbox("Choose a visualization type", ["Scatter Plot", "Bar Chart", "Line Chart", "Histogram", "Box Plot"])
columns = clean_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
if columns:
    x_axis = st.selectbox("Choose X-axis", columns)
    y_axis = st.selectbox("Choose Y-axis", columns)

    if viz_type == "Scatter Plot":
        fig = px.scatter(clean_data, x=x_axis, y=y_axis)
    elif viz_type == "Bar Chart":
        fig = px.bar(clean_data, x=x_axis, y=y_axis)
    elif viz_type == "Line Chart":
        fig = px.line(clean_data, x=x_axis, y=y_axis)
    elif viz_type == "Histogram":
        fig = px.histogram(clean_data, x=x_axis)
    elif viz_type == "Box Plot":
        fig = px.box(clean_data, x=x_axis, y=y_axis)
    st.plotly_chart(fig)
```

## Clustering Analysis

Using KMeans, we perform clustering on selected columns. Before applying KMeans, we standardize the data using `StandardScaler` to ensure that all features contribute equally to the distance calculations. The clusters are then visualized in a scatter plot, allowing us to see which groups emerge within the data.

```python
st.write("### Clustering Analysis")
if len(columns) > 1:
    cluster_features = st.multiselect("Choose features for clustering", columns, default=columns[:2])
    if len(cluster_features) >= 2:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clean_data[cluster_features])

        kmeans = KMeans(n_clusters=3)
        clusters = kmeans.fit_predict(scaled_data)
        clean_data['Cluster'] = clusters

        fig = px.scatter(clean_data, x=cluster_features[0], y=cluster_features[1], color='Cluster', title="Clustering Analysis")
        st.plotly_chart(fig)
```

## Predictive Analysis

In the predictive analysis section, users can select a target variable for a linear regression model. We use `Annual Purchase Amount` as the default target, along with selected features. We split the data into training and test sets, train a `LinearRegression` model, and calculate the mean squared error (MSE) on the test data. The app also displays actual vs. predicted values in a scatter plot for easy comparison.

```python
st.write("### Predictive Analysis (Linear Regression)")
target = st.selectbox("Choose a target variable for prediction", columns)
features = st.multiselect("Choose features for prediction", [col for col in columns if col != target])

if target and len(features) > 0:
    X = clean_data[features]
    y = clean_data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    st.write(f"Mean Squared Error on test set: {mse:.2f}")

    result_df = pd.DataFrame({"Actual": y_test, "Predicted": predictions})
    st.write("### Prediction Results")
    st.write(result_df.head(10))

    fig = px.scatter(result_df, x="Actual", y="Predicted", title="Actual vs Predicted")
    st.plotly_chart(fig)
```

## Summary Insights

Finally, the summary section provides a quick recap of the insights that can be gathered from the clustering and predictive analysis. These bullet points help orient users on how to interpret the results in the context of business or research.

```python
st.write("## Summary Insights")
st.write("- **Clustering** helps to identify natural groupings in the data.")
st.write("- **Predictive Analysis** can forecast trends based on selected features, providing actionable insights for future decisions.")
```
