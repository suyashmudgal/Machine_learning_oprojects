import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ----------------------------------
# Generate House Dataset
# ----------------------------------
def generate_house_data(n_samples=500):

    np.random.seed(50)

    size = np.random.randint(1000, 5000, n_samples)

    # Realistic price formula
    price = (
        size * 2500
        + np.random.randint(-300000, 300000, n_samples)
    )

    return pd.DataFrame({
        "Size": size,
        "Price": price
    })


# ----------------------------------
# Train Model
# ----------------------------------
@st.cache_resource
def train_model():

    df = generate_house_data()

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

    return model, metrics


# ----------------------------------
# Main App
# ----------------------------------
def main():

    st.set_page_config(
        page_title="House Price Prediction",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 House Price Prediction System")
    st.write(
        "Predict house prices using Linear Regression based on house size."
    )

    model, metrics = train_model()

    # ---------------- Metrics ----------------
    st.subheader("📊 Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{metrics['MAE']:,.0f}")
    col2.metric("MSE", f"{metrics['MSE']:,.0f}")
    col3.metric("R² Score", f"{metrics['R2']:.4f}")

    st.divider()

    # ---------------- User Input ----------------
    size = st.slider(
        "Select House Size (sq ft)",
        min_value=1000,
        max_value=5000,
        value=2000,
        step=100
    )

   
    if st.button("Predict Price"):

        prediction = model.predict([[size]])[0]

        st.success(
            f"💰 Predicted House Price: ₹{prediction:,.2f}"
        )

        
        df = generate_house_data()

       
        fig = px.scatter(
            df,
            x="Size",
            y="Price",
            title="House Size vs Price",
            trendline="ols"
        )

        # Predicted Point
        fig.add_scatter(
            x=[size],
            y=[prediction],
            mode="markers",
            marker=dict(
                size=15,
                color="red"
            ),
            name="Predicted House"
        )

        # Vertical Line
        fig.add_vline(
            x=size,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Size = {size}"
        )

        # Horizontal Line
        fig.add_hline(
            y=prediction,
            line_dash="dash",
            line_color="blue",
            annotation_text=f"₹{prediction:,.0f}"
        )

        fig.update_layout(
            xaxis_title="House Size (sq ft)",
            yaxis_title="House Price (₹)",
            height=650
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------- Details ----------------
        st.subheader("📋 Prediction Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"🏠 House Size: {size:,} sq ft")

        with col2:
            st.info(f"💰 Estimated Price: ₹{prediction:,.2f}")

        # ---------------- Dataset Preview ----------------
        with st.expander("📄 View Sample Dataset"):
            st.dataframe(df.head(20))


if __name__ == "__main__":
    main()