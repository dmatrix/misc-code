import tensorflow as tf
import pandas as pd
import mlflow.tensorflow
import mlflow.pyfunc

if __name__== '__main__':
    # Read data
    mnist = tf.keras.datasets.mnist
    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    # Build the model
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=1)
    model.evaluate(x_test, y_test)
    # Save the model
    tempdir = '/tmp/model'
    model.save(tempdir)
    model = tf.keras.models.load_model(tempdir)
    # Log and load the model to mlflow
    mlflow.set_tracking_uri('mlruns')
    mlflow.set_experiment('Default')
    run = mlflow.start_run()
    mlflow.tensorflow.log_model(
            tf_saved_model_dir=tempdir,
            tf_meta_graph_tags=None,
            tf_signature_def_key='serving_default',
            artifact_path='model'
    )
    mlflow.end_run()
    model_uri = f'mlruns/0/{run.info.run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(model_uri)
    # Invoke the model
    # It causes "__call__() keywords must be strings"
    n1, n2, n3 = x_test.shape
    df = pd.DataFrame(x_test.reshape(n1, n2*n3))
    try:
        print('----- Predict -------')
        print(model.predict(df))
    except Exception as e:
        print(e)
    # Invoke the model with string typed columns
    # It raises "# Expected argument names ['flatten_1_input']"
    n1, n2, n3 = x_test.shape
    df = pd.DataFrame(data=x_test.reshape(n1, n2*n3), columns=[str(c) for c in range(n2*n3)])
    try:
        print('----- Predict with string typed columns -----')
        print(model.predict(df))
    except Exception as e:
        print(e)
