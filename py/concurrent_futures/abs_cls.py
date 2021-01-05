import os
import sys
import time
import requests
from abc import abstractmethod

POP20_CC = ('CN IN US ID BR PK NG BD AU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

# URL site to scrap the flags from
BASE_URL = 'http://flupy.org/data/flags'

# Save flag images in this local directory
DEST_DIR = 'downloads/'


class AbstractDownloader:

    def __init__(self):
        pass

    def save_flag(self, img, filename):
        path = os.path.join(DEST_DIR, filename)
        with open(path, 'wb') as fp:
            fp.write(img)

    def get_flag(self, cc):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        resp = requests.get(url)
        return resp.content

    def show(self, text):
        print(text, end=' ')
        sys.stdout.flush()

    def main(self, func):
        t0 = time.time()
        count = func(POP20_CC)
        elapsed = time.time() - t0
        msg = '\n{} flags downloaded in {:.2f}s'
        print(msg.format(count, elapsed))

    @abstractmethod
    def download_many(self, cc_list):
        pass
