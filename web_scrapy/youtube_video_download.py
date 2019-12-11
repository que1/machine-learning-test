#!/usr/bin/env python3
# -*- coding: utf8 -*-

from pytube import YouTube

def download_video(url, path):
    yt = YouTube(url)

    player_config_args = yt.player_config_args
    print("author: " + player_config_args['player_response']['videoDetails']['author'])
    print("video_id: " + player_config_args['player_response']['videoDetails']['videoId'])
    print("watch_url: " + yt.watch_url)
    print("title: " + player_config_args['player_response']['videoDetails']['title'])

    stream = yt.streams.first()
    # stream.download(output_path=path)

    print("download_url: " + stream.url)






if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=YqXFXx-PjUQ"
    path = "/Users/q/doc/video_clip/"
    print("-------------begin-------------")
    download_video(url, path)
    print("------------- end -------------")