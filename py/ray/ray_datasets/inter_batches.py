import ray

if __name__ == "__main__":
    epochs = ray.data.range(10).repeat(5).iter_epochs()
    for i, epoch in enumerate(epochs):
        print("Epoch", i)
        for row in epoch.iter_rows():
            print(row)