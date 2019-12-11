#!/usr/bin/env python3
# -*- coding: utf8 -*-

from pytube import YouTube

def download_video(url, local_file_path):
    yt = YouTube(url)
    stream = yt.streams.first()

    player_config_args = yt.player_config_args
    author = player_config_args['player_response']['videoDetails']['author']
    video_id = player_config_args['player_response']['videoDetails']['videoId']  #yt.video_id
    watch_url = yt.watch_url
    title = player_config_args['player_response']['videoDetails']['title']       #yt.title
    filename_prefix = author + " -- "

    print("author: " + author)
    print("video_id: " + video_id)
    print("watch_url: " + watch_url)
    print("title: " + title)
    print("download_url: " + stream.url)
    print("local_file_path: {0}{1}{2}.mp4".format(local_file_path, filename_prefix, title))
    stream.download(output_path=local_file_path, filename_prefix=filename_prefix)


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=uN8ekr2nF8s"
    local_file_path = "/Users/q/doc/video_clip/"
    print("-------------begin-------------")
    download_video(url, local_file_path)
    print("------------- end -------------")