from concurrent import futures

from sync import save_flag, get_flag, show, main

# Number of threads to be used by ThreadPoolExecutor
MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:

        # Map over the list of countries, downloading each flag separately in
        # thread from the tread pool
        res = executor.map(download_one, sorted(cc_list))
        return len(list(res))


if __name__ == '__main__':
    main(download_many)
