import tensorflow as tf
import pandas as pd
import mlflow.tensorflow
import mlflow.pyfunc

def predict_pyfunc(model_uri, verbose=False):

    print("+-" * 70)
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
    cols = [str(c) for c in range(n2 * n3)]
    predictions = pyfunc_model.predict(pd.DataFrame(data=new_x_test, columns=cols))
    print("+-" * 70)
    print(f"predictions = {predictions}")
    print("+-" * 70)

def predict_mlflow_tf(model_uri, verbose=False):
    tf_graph = tf.Graph()
    tf_sess = tf.Session(graph=tf_graph)
    with tf_graph.as_default():
        signature_definition = mlflow.tensorflow.load_model(model_uri=model_uri,
                                                            tf_sess=tf_sess)
        input_tensors = [tf_graph.get_tensor_by_name(input_signature.name)
                         for _, input_signature in signature_definition.inputs.items()]
        output_tensors = [tf_graph.get_tensor_by_name(output_signature.name)
                          for _, output_signature in signature_definition.outputs.items()]
        print(output_tensors)

# Read data
if __name__== '__main__':
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
    tf_models = './tf_models'
    model.save(tf_models)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.tensorflow.log_model(
            tf_saved_model_dir=tf_models,
            tf_meta_graph_tags=None,
            tf_signature_def_key='serving_default',
            artifact_path='model')

    model_uri = f'runs:/{run.info.run_id}/model'
    # predict_pyfunc(model_uri)
    predict_mlflow_tf(model_uri)
