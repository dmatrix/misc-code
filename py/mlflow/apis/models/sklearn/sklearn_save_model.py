import numpy as np
import pickle

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import mlflow

# source: https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html
# This example workflow shows to work with an existing model in native format, load
# into memory, log and register the model with MLflow-built sklearn MLflow APIs.

# 1. Create a simple linear regression model using sklearn APIs
# 2. Save the model in native pickle format
# 3. Load back the saved model
# 4. Log and register the model in the model registry
# 5. Load back from the model registry and score the model

# Load the diabetes dataset
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

# Use only one feature
diabetes_X = diabetes_X[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]


def print_predictions(m, y_pred):

    # The coefficients
    print('Coefficients: \n', m.coef_)
    # The mean squared error
    print('Mean squared error: %.2f'
          % mean_squared_error(diabetes_y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f'
          % r2_score(diabetes_y_test, y_pred))


if __name__ == '__main__':
    # Create linear regression object
    lr_model = linear_model.LinearRegression()

    # Train the model using the training sets
    lr_model.fit(diabetes_X_train, diabetes_y_train)

    # Make predictions using the testing set
    diabetes_y_pred = lr_model.predict(diabetes_X_test)
    print_predictions(lr_model, diabetes_y_pred)

    # save the model in the native sklearn format
    filename = 'lr_model.pkl'
    pickle.dump(lr_model, open(filename, 'wb'))

    # load the model into memory
    loaded_model = pickle.load(open(filename, 'rb'))

    # log and register the model using MLflow scikit-learn API
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    reg_model_name = "SklearnLinearRegression"
    with mlflow.start_run():
        mlflow.sklearn.log_model(loaded_model, "sk_learn",
                                 serialization_format="cloudpickle",
                                 registered_model_name=reg_model_name)

    # load the model from the model registry and score
    model_uri = f"models:/{reg_model_name}/1"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    print("--")

    # Make predictions using the testing set
    diabetes_y_pred = loaded_model.predict(diabetes_X_test)
    print_predictions(loaded_model, diabetes_y_pred)
