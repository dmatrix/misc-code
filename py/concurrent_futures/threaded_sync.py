from abs_cls import AbstractDownloader
from concurrent import futures

# Number of threads to be used by ThreadPoolExecutor
MAX_WORKERS = 20


class ThreadedDownloader(AbstractDownloader):

    def __init__(self):
        super(ThreadedDownloader, self).__init__()

    def download_one(self, cc):
        image = self.get_flag(cc)
        self.show(cc)
        self.save_flag(image, cc.lower() + '.gif')
        return cc

    def download_many(self, cc_list):
        workers = min(MAX_WORKERS, len(cc_list))
        with futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Map over the list of countries, downloading each flag separately in
            # thread from the tread pool
            res = executor.map(self.download_one, sorted(cc_list))
            return len(list(res))

    def main_thr(self):
        self.main(self.download_many)


if __name__ == '__main__':

    threaded_downloader = ThreadedDownloader()
    threaded_downloader.main_thr()
