"""
Lazy file reader using yield example. This can be used as an example for large files to be read in
chunks. PyTorch's Dataloader class uses this
"""


def read_in_chunks(file_object, chunk_size=1024):
    """
    Lazy function (generator) to read a file in chunks
    Default size: 1k
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_chunk(data):
    print(data)


if __name__ == '__main__':
    with open('data/sample-2mb-text-file.txt') as f:
        for piece in read_in_chunks(f):
            process_chunk(piece)

