from threaded_sync import ThreadedDownloader, MAX_WORKERS
from concurrent import futures


class FuturesDownloader(ThreadedDownloader):
    def __init__(self):
        super(FuturesDownloader, self).__init__()

    def download_many(self, cc_list):
        with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # tasks to do
            to_do = []
            for cc in sorted(cc_list):
                # create a future, schedule it, and append to the to_do list
                future = executor.submit(self.download_one, cc)
                to_do.append(future)
                msg = 'Scheduled for {}: {}'
                print(msg.format(cc, future))

            # tasks already completed using as_completed
            results = []
            for future in futures.as_completed(to_do):
                # yields results as completed
                res = future.result()
                msg = '{} result: {!r}'
                print(msg.format(future, res))
                results.append(res)
        return len(results)


if __name__ == '__main__':
    futures_downloader = FuturesDownloader()
    futures_downloader.main_thr()
