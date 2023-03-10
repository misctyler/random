import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder

data = pd.read_csv('turntable/Record-Collection.csv')


# Create a dataset
x = np.array([[1], [2], [3], [4]])
y = np.array([[0], [-1], [-2], [-3]])

# Create a model
model = Sequential()
model.add(Dense(units=1, input_shape=(1,)))

# Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error')

# Train the model
model.fit(x, y, epochs=100)

# Use the model to make predictions
print(model.predict([[6]]))
print(data.columns)