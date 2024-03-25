#---- Imports -----
import my_flask_app.DBHandler as DBHandler
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, MaxNLocator
#---- Imports -----

lm = LinearRegression()

dataset = DBHandler.getMostPopularVideosByCountryAll()
dataset.sort_values(by="Views", ascending=True, inplace=True)

# Split data into Features and Target
x_data = dataset[["Views", "Comment_Count", "Duration"]].to_numpy()
y_data = dataset["Like_Count"].to_numpy()

def trainModel():
    lm.fit(x_data, y_data)

def predict(views, comments):
    print("tbd")

def test():
    print(x_data)