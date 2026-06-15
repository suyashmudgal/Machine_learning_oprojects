import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------------
# Generate Sample House Data
# -----------------------------
def generate_house_data(n_samples=100):

    np.random.seed(50)

    size = np.random.randint(1000, 5000, n_samples)

    # Realistic relationship between size and price
    price = (
        size * 2500
        + np.random.randint(-300000, 300000, n_samples)
    )

    return pd.DataFrame({
        "Size": size,
        "Price": price
    })


# -----------------------------
# Train and Save Model
# -----------------------------
def train_model():

    df = generate_house_data(500)

    X = df[["Size"]]
    y = df["Price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, predictions),
        "MSE": mean_squared_error(y_test, predictions),
        "R2": r2_score(y_test, predictions)
    }

    with open("house_model.pkl", "wb") as file:
        pickle.dump(model, file)

    return model, metrics


# -----------------------------
# Load Model
# -----------------------------
def load_model():

    if not os.path.exists("house_model.pkl"):
        model, _ = train_model()
        return model

    with open("house_model.pkl", "rb") as file:
        model = pickle.load(file)

    return model


# -----------------------------
# Streamlit App
# -----------------------------
def main():

    st.set_page_config(
        page_title="House Price Predictor",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 House Price Prediction System")

    st.write(
        "Enter the size of a house and predict its estimated price using Linear Regression."
    )

    # Train model once and get metrics
    model, metrics = train_model()

    st.subheader("📊 Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{metrics['MAE']:,.0f}")
    col2.metric("MSE", f"{metrics['MSE']:,.0f}")
    col3.metric("R² Score", f"{metrics['R2']:.4f}")

    st.divider()

    size = st.number_input(
        "Enter House Size (sq ft)",
        min_value=500,
        max_value=10000,
        value=1500,
        step=100
    )

    if st.button("Predict Price"):

        prediction = model.predict([[size]])[0]

        st.success(
            f"💰 Predicted House Price: ₹{prediction:,.2f}"
        )

        # Generate data for graph
        df = generate_house_data(500)

        fig = px.scatter(
            df,
            x="Size",
            y="Price",
            title="House Size vs Price",
            trendline="ols"
        )

        fig.add_scatter(
            x=[size],
            y=[prediction],
            mode="markers",
            marker=dict(
                size=15,
                color="red"
            ),
            name="Your Prediction"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("📋 House Details")

        st.write(f"**Size:** {size:,} sq ft")
        st.write(f"**Estimated Price:** ₹{prediction:,.2f}")


if __name__ == "__main__":
    main()