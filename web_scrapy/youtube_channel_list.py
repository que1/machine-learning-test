#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://www.google.com.hk/'
    }
    response = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(response.content, "html5lib")
    scriptList = bsObj.findAll("script")

    needObj = None
    for script in scriptList:
        if script.get_text().find("gridVideoRenderer") >= 0:
            needObj = script
        else:
            continue

    if needObj == None:
        print("--------None--------")
    else:
        js_code = str(needObj.get_text())
        get_yt_initial_data(js_code)


def get_yt_initial_data(js_code):
    print(js_code)
    lines = js_code.split("window[\"ytInitialPlayerResponse")
    if len(lines) >= 1:
        line = lines[0]
        str = line.replace("window[\"ytInitialData\"] = ", "").replace(";", "").strip()
        parse_yt_inital_data_json(str)


def parse_yt_inital_data_json(init_data):
    print(init_data)
    json_obj = json.loads(init_data)
    tabRenderer_list = json_obj['contents']['twoColumnBrowseResultsRenderer']['tabs']
    for tabRenderer in tabRenderer_list:
        if 'tabRenderer' in tabRenderer.keys():
            tab = tabRenderer['tabRenderer']
            if tab['selected'] == True:
                content = tab['content']
                section_list_renderer = content['sectionListRenderer']
                section_contents =  section_list_renderer['contents']
                item_section_renderer = section_contents[0]['itemSectionRenderer']
                item_contents = item_section_renderer['contents']
                grid_renderer = item_contents[0]['gridRenderer']
                items = grid_renderer["items"]
                for item in items:
                    grid_video_renderer = item['gridVideoRenderer']
                    video_id = grid_video_renderer["videoId"]
                    print(video_id)




if __name__ == '__main__':
    channel_url = "https://www.youtube.com/user/BobaTurbo/videos"
    get_html(channel_url)
