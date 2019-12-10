#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
from contextlib import closing


def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        r.encoding = "utf-8"
        chunk_size = 10240
        content_size = int(r.headers['content-length'])
        print('--------开始下载--------')
        with open(path, "wb") as f:
            n = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = n*10240.0/content_size
                f.write(chunk)
                f.flush()
                #os.fsync(f.fileno())
                if n % 100 == 0:
                    print('已下载{0:%}'.format(loaded))
                n += 1
        print('--------结束下载--------')


if __name__ == '__main__':
    url = "https://video.pearvideo.com/mp4/adshort/20191204/cont-1629430-14663791_adpkg-ad_hd.mp4"
    path = "/Users/q/doc/video_clip/1233.mp4"
    download_file(url, path)







