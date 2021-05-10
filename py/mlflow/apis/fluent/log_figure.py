import mlflow
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.plot([0, 1], [2, 3])

    with mlflow.start_run():
        mlflow.log_figure(fig, "figure.png")
