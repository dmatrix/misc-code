from abs_cls import AbstractDownloader


class SyncDownloader(AbstractDownloader):
    def __init__(self):
        super(SyncDownloader, self).__init__()

    def download_many(self, cc_list):
        for cc in sorted(cc_list):
            image = self.get_flag(cc)
            self.show(cc)
            self.save_flag(image, cc.lower() + '.gif')

        return len(cc_list)


if __name__ == '__main__':

    sync_downloader = SyncDownloader()
    sync_downloader.main(sync_downloader.download_many)
