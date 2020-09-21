import mlflow

if __name__ == '__main__':

    with open('test.txt', 'w') as test_file:
      test_file.write('1')
    mlflow.log_artifact('test.txt', 'test')
    mlflow.log_param('p', 1)
    with open('test.txt', 'w') as test_file:
      test_file.write('2')
    mlflow.log_artifact('test.txt', 'test')
    mlflow.log_param('p2', 2)
