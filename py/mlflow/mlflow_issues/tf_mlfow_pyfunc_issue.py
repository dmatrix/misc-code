import pandas as pd
import mlflow.keras
import mlflow.pyfunc
import keras

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
    predictions = pyfunc_model.predict(pd.DataFrame(data=x_test))
    print("+-" * 25)
    print(f"predictions = {predictions}")
    print("+-" * 25)

if __name__== '__main__':
    # Read data
    mnist = keras.datasets.mnist
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
    run_id = None
    with mlflow.start_run() as run:
        mlflow.keras.autolog()
        model.fit(x_train, y_train, epochs=1)
        model.evaluate(x_test, y_test)
        run_id = run.info.run_id

    model_uri = f'runs:/{run.info.run_id}/model'
    predict_pyfunc(model_uri, verbose=True)
