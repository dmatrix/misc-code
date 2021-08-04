def bootstrap():
    from pathlib import Path
    import os

    path = Path(os.getcwd())
    file_path = path / "config.yaml"
    driver_entities = [1001, 1002, 1003, 1004, 1005]
    with open(file_path, "w") as f:
        for driver in driver_entities:
            f.write(f"driver: {str(driver)}")
            f.write("\n")


if __name__ == '__main__':
    bootstrap()

