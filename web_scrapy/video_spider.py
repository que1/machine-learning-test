#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
from contextlib import closing
import time


def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        r.encoding = "utf-8"
        chunk_size = 10240
        content_size = int(r.headers['content-length'])
        print('--------开始下载--------')
        with open(path, "wb") as f:
            p = ProgressData(size = content_size, unit = 'Kb', block = chunk_size)
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                p.output()
        print('--------结束下载--------')


class ProgressData:

    def __init__(self, block, size, unit, file_name='', ):
        self.block = block/1000.0
        self.size = size/1000.0
        self.unit = unit
        self.file_name = file_name
        self.count = 0
        self.start = time.time()

    def output(self):
        self.end = time.time()
        self.count += 1
        speed = self.block/(self.end - self.start) if(self.end - self.start) > 0 else 0
        self.start = time.time()
        loaded = self.count * self.block
        progress = round(loaded/self.size, 4)
        if loaded >= self.size:
            print('%s下载完成\r\n', self.file_name)
        else:
            print('{0}下载进度{1:.2f}{2}/{3:.2f}{4} {5:.2%} 下载速度{6:.2f}{7}/s'.format(self.file_name, loaded, self.unit, self.size, self.unit, progress, speed, self.unit))
            print('%50s'%('/'*int((1 - progress) * 50)))





if __name__ == '__main__':
    # url = "https://video.pearvideo.com/mp4/adshort/20191204/cont-1629430-14663791_adpkg-ad_hd.mp4"
    url = 'https://r5---sn-i3beln7k.googlevideo.com/videoplayback?expire=1576061290&ei=CnXwXc_hH4fcgQPeuoCIAg&ip=103.201.24.187&id=o-ABZI4u9iu6n8pmMhhNAfIoDjspcJdPyQnHzfDJu2X1bZ&itag=22&source=youtube&requiressl=yes&mm=31,26&mn=sn-i3beln7k,sn-npoe7n7r&ms=au,onr&mv=m&mvi=4&pl=24&initcwndbps=466250&mime=video/mp4&ratebypass=yes&dur=908.387&lmt=1565812023351757&mt=1576030336&fvip=5&fexp=23842630&c=WEB&txp=2316222&sparams=expire,ei,ip,id,itag,source,requiressl,mime,ratebypass,dur,lmt&sig=ALgxI2wwRAIgNO_6_cnaP76aqU8-0P7pGSSMB0CLwXzhWVgBgveWM90CIF2MKhYxSBhztvQDprO_S1sJpCRYtFkFmkViBVdcc3KH&lsparams=mm,mn,ms,mv,mvi,pl,initcwndbps&lsig=AHylml4wRgIhALZxgG1Y76BpVtceGenPlWzLMbBWotwpsl4ArDsg8FEBAiEA9XnerJaiQRML84naNQE3Fl5qNF8jBSJZHqUp2rtdCMk='
    path = "/Users/q/doc/video_clip/1235.mp4"
    download_file(url, path)







