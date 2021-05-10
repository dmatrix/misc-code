import mlflow

if __name__ == '__main__':

    with mlflow.start_run():

        # Log HTML text
        mlflow.log_text("<a href=https://mlflow.org>MLflow Website</a>", "mlflow.html")
