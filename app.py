import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Title and description
st.title("PipeDreams - Enhanced Data Explorer")
st.write("Upload a CSV file to analyze, visualize, and extract deeper insights from your data using ETL and machine learning.")

# Load sample data if no file is uploaded
sample_data_path = "data/customers-100000.csv"

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("## Uploaded Data")
else:
    # Use sample data if no file is uploaded
    st.write("No file uploaded. Displaying sample data.")
    data = pd.read_csv(sample_data_path)
    st.write("## Sample Data")
st.write(data.head())  # Display the first few rows of the data

# Basic ETL Transformations
st.write("## ETL Transformations")

# Remove rows with missing values
clean_data = data.dropna()
st.write("### Cleaned Data (no missing values)")
st.write(clean_data.head())

# Convert Subscription Date to datetime and add 'Years Since Subscription' feature
if 'Subscription Date' in clean_data.columns:
    clean_data['Subscription Date'] = pd.to_datetime(clean_data['Subscription Date'], errors='coerce')
    clean_data['Years Since Subscription'] = (pd.to_datetime("today") - clean_data['Subscription Date']).dt.days / 365
    st.write("### Added 'Years Since Subscription' Feature")
    st.write(clean_data[['Subscription Date', 'Years Since Subscription']].head())

# Encode categorical columns as integers to make them usable in ML
label_encoders = {}
for column in clean_data.select_dtypes(include=['object']).columns:
    if column != 'Subscription Date' and column != 'Email' and column != 'Website':  # Exclude specific non-informative columns
        le = LabelEncoder()
        clean_data[column] = le.fit_transform(clean_data[column])
        label_encoders[column] = le
st.write("### Categorical Columns Encoded")
st.write(clean_data.head())

# Generate synthetic target column for regression analysis
np.random.seed(42)
clean_data['Annual Purchase Amount'] = np.random.normal(loc=5000, scale=2000, size=len(clean_data)).clip(min=0)

# Data Visualization
st.write("## Data Visualization")

# Select visualization type
viz_type = st.selectbox("Choose a visualization type", ["Scatter Plot", "Bar Chart", "Line Chart", "Histogram", "Box Plot"])

# Select columns for visualization
columns = clean_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
if columns:
    x_axis = st.selectbox("Choose X-axis", columns)
    y_axis = st.selectbox("Choose Y-axis", columns)

    # Generate the selected plot
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
else:
    st.write("No numerical data available for visualization.")

# Advanced Insights
st.write("## Advanced Insights with Machine Learning")

# Clustering Analysis
st.write("### Clustering Analysis")
if len(columns) > 1:
    cluster_features = st.multiselect("Choose features for clustering", columns, default=columns[:2])
    if len(cluster_features) >= 2:
        # Standardize features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clean_data[cluster_features])

        # Run KMeans
        kmeans = KMeans(n_clusters=3)
        clusters = kmeans.fit_predict(scaled_data)
        clean_data['Cluster'] = clusters

        # Plot clusters
        fig = px.scatter(clean_data, x=cluster_features[0], y=cluster_features[1], color='Cluster', title="Clustering Analysis")
        st.plotly_chart(fig)
    else:
        st.write("Please select at least two features for clustering.")
else:
    st.write("Not enough numerical features for clustering.")

# Predictive Analysis
st.write("### Predictive Analysis (Linear Regression)")
target = st.selectbox("Choose a target variable for prediction", columns)
features = st.multiselect("Choose features for prediction", [col for col in columns if col != target])

# Ensure Annual Purchase Amount appears as a default target option
if 'Annual Purchase Amount' not in columns:
    st.write("No appropriate target variable found. Consider adding synthetic or numerical data.")

if target and len(features) > 0:
    X = clean_data[features]
    y = clean_data[target]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict and evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    st.write(f"Mean Squared Error on test set: {mse:.2f}")

    # Display predictions and a visual comparison
    result_df = pd.DataFrame({"Actual": y_test, "Predicted": predictions})
    st.write("### Prediction Results")
    st.write(result_df.head(10))

    # Scatter plot of Actual vs Predicted
    fig = px.scatter(result_df, x="Actual", y="Predicted", title="Actual vs Predicted")
    st.plotly_chart(fig)

# Insight Summary
st.write("## Summary Insights")
st.write("Based on the clustering and predictive analysis, here are some insights that could help in decision-making:")
st.write("- **Clustering** helps to identify natural groupings in the data.")
st.write("- **Predictive Analysis** can forecast trends based on selected features, providing actionable insights for future decisions.")
