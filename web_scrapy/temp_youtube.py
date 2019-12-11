#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests

def get_html(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    print(response.content)


if __name__ == '__main__':
    channel_url = 'https://www.youtube.com/channel/UCHwSpDbtOUrx9hXIljaN9xg/videos'
    get_html(channel_url)