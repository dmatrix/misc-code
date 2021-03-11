import nltk
import mlflow

if __name__ == '__main__':
    nltk.download('punkt')
    # Write all files in downloaded in the destination directory to root artifact_uri/
    with mlflow.start_run():
        mlflow.log_artifacts("/Users/julesdamji/nltk_data", artifact_path="nltk")
