import shutil

artifact_path = "artifacts/models/delete_file.mdl"

if __name__ == "__main__":

    try:
        shutil.rmtree(artifact_path)
    except OSError as err:
        print('{}. Failed to permanently delete artifacts. Continuing with gc ...'.format(err))



