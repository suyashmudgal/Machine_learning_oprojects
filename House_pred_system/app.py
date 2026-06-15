import numpy as np
import streamlit as st
import pandas as pd
import pickle

def generate_house_data(n_sample = 100):
    np.random.seed(50)
    size = np.random.randint(1000, 5000, n_sample   )
    price = np.random.randint(100000, 10000000, n_sample)
    data = pd.DataFrame({'Size': size, 'Price': price})
    return data

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score