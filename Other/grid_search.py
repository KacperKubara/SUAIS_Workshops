"""Grid Search Example based on the Random Forest Regression"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# Read Data
from sklearn.datasets import load_boston 
dataset = load_boston() #Loading Sklearn internal dataset

# Choose which features to use
x = dataset["data"][:, [7, 9]] # using DIS and TAX features
y = dataset["target"]     # output value

# Split data into train and test dataset
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x[:,:], y, test_size = 0.2, random_state = 42)

# Data Preprocessing
from sklearn.preprocessing import StandardScaler
sc_x    = StandardScaler()
x_train = sc_x.fit_transform(x_train) # Scaling the data
x_test  = sc_x.transform(x_test)

# Train Model with the Grid Search
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
""" You can take any parameters to sweep through
 as long as they're available in the specific model"""

parameters = {'n_estimators': [5, 10, 50, 75, 100],
                'min_samples_split': [2, 3, 4, 5],
                'min_samples_leaf': [1, 2, 3, 4, 5]}

random_forest = GridSearchCV( estimator = RandomForestRegressor(),
                              param_grid = parameters, cv = 5)


# Train the model
random_forest.fit(x_train, y_train)
best_parameters = random_forest.best_params_

# Predict the model
y_pred = random_forest.predict(x_test)

# Measure Accuracy
from sklearn.metrics import mean_squared_error
acc = mean_squared_error(y_test, y_pred)

# Visualise Results
from mpl_toolkits.mplot3d import axes3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('DIS values')
ax.set_ylabel('TAX values')
ax.set_zlabel('House Price(1k$)')
x_test = sc_x.inverse_transform(x_test)
ax.scatter(x_test[:,0], x_test[:,1], y_test, color = 'r')
ax.scatter(x_test[:,0], x_test[:,1], y_pred, color = 'b')
plt.show()