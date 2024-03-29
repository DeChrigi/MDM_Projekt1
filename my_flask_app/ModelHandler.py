#---- Imports -----
import DBHandler as DBHandler
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, MaxNLocator
import pickle
#---- Imports -----

lm = LinearRegression()

dataset = DBHandler.getMostPopularVideosByCountryAll()
dataset.sort_values(by="Like_Count", ascending=True, inplace=True)

# Split data into Features and Target
x_data = dataset[["Views", "Comment_Count", "Duration"]].to_numpy()
y_data = dataset["Like_Count"].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.20, random_state=42)

lm.fit(x_train, y_train)

y_pred_lr = lm.predict(x_test)
r2 = r2_score(y_test, y_pred_lr)
mse = mean_squared_error(y_test, y_pred_lr)

def predict(views, comments, duration):
    input_data = [[views, comments, duration]]

    predicted_likes = lm.predict(input_data)

    return predicted_likes

# save the classifier
with open('LinearRegressor.pkl', 'wb') as fid:
    pickle.dump(lm, fid)    

# load it again
with open('LinearRegressor.pkl', 'rb') as fid:
    gbr_loaded = pickle.load(fid)