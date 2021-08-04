def bootstrap():
    from pathlib import Path
    import os

    path = Path(os.getcwd())
    file_path = path / "driver.yaml"
    config_path = path/ "config.yaml"
    driver_entities = [1001, 1002, 1003, 1004, 1005]
    configs = {"path": os.getcwd(),
              "provider": "local",
              "online": True
              }
    with open(file_path, "w") as f:
        for driver in driver_entities:
            f.write(f"driver: {str(driver)}")
            f.write("\n")
    with open(config_path, "w") as f:
        for k, v in configs.items():
            f.write("".join([str(k),":",str(v),"\n"]))


if __name__ == '__main__':
    bootstrap()

