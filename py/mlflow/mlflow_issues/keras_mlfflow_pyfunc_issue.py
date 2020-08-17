import keras
import pandas as pd
import mlflow.pyfunc
import mlflow.keras

def predict_pyfunc(model_uri, verbose=False):

    print("+-" * 25)
    if verbose:
        print(f"x_type= {type(x_test)}")
        print(f"x_test shape={x_test.shape}")
        print(f"x_test  dim={x_test.ndim}")
        print(f"y_test shape={y_test.shape}")
        print(f"y_test  dim={y_test.ndim}")
    n1, n2, n3 = x_test.shape
    new_x_test = x_test.reshape(n1, n2 * n3)
    if verbose:
        print(f"x_test new shape={new_x_test.shape}")
        print(f"x_test new dim={new_x_test.ndim}")

    pyfunc_model = mlflow.pyfunc.load_model(model_uri, suppress_warnings=True)
    # cols = [str(c) for c in range(n2 * n3)]
    # predictions = pyfunc_model.predict(pd.DataFrame(data=new_x_test, columns=cols))
    predictions = pyfunc_model.predict(pd.DataFrame(x_test))

    print("+-" * 25)
    print(f"predictions for Keras PyFunc Load Model= {predictions}")
    print("+-" * 25)

def predict_mlflow_keras(model_uri):

    keras_model = mlflow.keras.load_model(model_uri)
    predictions = keras_model.predict(x_test)
    print("+-" * 25)
    print(f"predictions for Keras Load Model= {predictions}")
    print("+-" * 25)

if __name__== '__main__':
    # Read data
    mnist = keras.datasets.mnist
    input_shape = (28, 28, 1)
    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Build the model
    model = keras.models.Sequential([
      keras.layers.Flatten(input_shape=(28, 28)),
      keras.layers.Dense(128, activation='relu'),
      keras.layers.Dropout(0.2),
      keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=1)
    model.evaluate(x_test, y_test)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.keras.log_model(model,artifact_path='model')

    model_uri = f'runs:/{run.info.run_id}/model'

    predict_mlflow_keras(model_uri)
    predict_pyfunc(model_uri, verbose=True)
