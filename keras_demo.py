import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

# Create a dataset
x = np.array([[1], [2], [3], [4]])
y = np.array([[0], [-1], [-2], [-3]])

# Create a model
model = Sequential()
model.add(Dense(units=1, input_shape=(1,)))

# Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error')

# Train the model
model.fit(x, y, epochs=1000)

# Use the model to make predictions
print(model.predict([[5]]))