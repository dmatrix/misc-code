import os
import time
import sys

import requests

# 20 Popular and populous countries

POP20_CC = ('CN IN US ID BR PK NG BD AU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

# URL site to scrap the flags from
BASE_URL = 'http://flupy.org/data/flags'

# Save flag images in this local directory
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(func):
    t0 = time.time()
    count = func(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


#
# Synchronously download each country's flag
#
if __name__ == '__main__':
    main(download_many)



