import tensorflow as tf

def predict_tf_native(model_dir, verbose=False):
    model = tf.keras.models.load_model(model_dir)
    predictions = model.predict(x_test[:5])
    print("+-" * 70)
    if verbose:
        print(f"type={type(x_test)}")
        print(f"shape={x_test.shape}")
        print(f"dim={x_test.ndim}")
        print(f"preditions dim={predictions.ndim}")
        print(f"preditions shape={predictions.shape}")
    print(f"predictions = {predictions}")
    print("+-" * 70)


if __name__ == '__main__':
    # Read data
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
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
    predict_tf_native(tempdir, verbose=True)
