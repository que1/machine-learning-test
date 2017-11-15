#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib
from bs4 import BeautifulSoup
import re
import time


class BlockInfo:

    blockIndex = 0
    blockName = ""
    blockPosition = ""
    blockBusiCircle = ""
    blockTag = ""
    blockDealUrl = ""

    def __init__(self):
        pass

    def toString(self):
        return "{0},{1},{2},{3},{4},{5}".format(self.blockIndex, self.blockName, self.blockPosition, self.blockBusiCircle, self.blockTag, self.blockDealUrl)


class HouseInfo:

    blockIndex = 0
    blockName = ""
    blockPosition = ""
    blockBusiCircle = ""
    blockTag = ""
    blockDealUrl = ""
    houseIndex = 0
    houseName = ""
    dealDate = ""
    totalPrice = ""
    unitPrice = ""
    listingPrice = ""
    positionInfo = ""
    dealHouseTime = ""
    dealCycleTime = ""
    houseDealUrl = ""

    def __init__(self, blockInfo):
        self.blockIndex = blockInfo.blockIndex
        self.blockName = blockInfo.blockName
        self.blockPosition = blockInfo.blockPosition
        self.blockBusiCircle = blockInfo.blockBusiCircle
        self.blockTag = blockInfo.blockTag
        self.blockDealUrl = blockInfo.blockDealUrl

    def toString(self):
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}".format(self.blockIndex, self.blockName, self.blockPosition, self.blockBusiCircle, self.blockTag,
                                                                    self.houseIndex, self.houseName, self.dealDate,
                                                                    self.totalPrice, self.unitPrice,
                                                                    self.positionInfo,
                                                                    self.dealHouseTime, self.dealCycleTime,
                                                                    self.houseDealUrl, self.blockDealUrl)


class ScrapyTest:

    baseBlockUrl = "http://bj.lianjia.com/xiaoqu/pg{0}"
    baseDealHouseUrl = "https://bj.lianjia.com/chengjiao/pg{0}c{1}"

    blockIndex = 0
    blockInfoList = []
    houseIndex = 0
    houseInfoList = []

    file = None

    def __init__(self):
        pass

    def __del__(self):
        self.file.close()

    def beginScrapyBlock(self):
        self.file = self.createIncrementFile()
        for i in range(1, 80):
            url = self.baseBlockUrl.format(i)
            bsObj = self.getBeautifulSoupObject(url)
            self.getBlockInfo(bsObj)
            time.sleep(10)

    def beginScrapyHouse(self):
        for blockInfo in self.blockInfoList:
            bsObj = self.getBeautifulSoupObject(blockInfo.blockDealUrl)
            self.getDealHouseInfo(bsObj, blockInfo)
            time.sleep(10)

    def getBeautifulSoupObject(self, url):
        try:
            html = urllib.request.urlopen(url)
        except urllib.error as e:
            return None
        try:
            bsObj = BeautifulSoup(html.read(), "html5lib")
        except AttributeError as e:
            return None
        return bsObj

    # block
    def getBlockInfo(self, bsObj):
        htmlClassInfoList = bsObj.findAll("div", {"class" : "info"})
        for htmlClassInfo in htmlClassInfoList:
            blockInfo = BlockInfo()
            blockInfo.blockIndex = self.blockIndex
            self.getBlockDetail(htmlClassInfo, blockInfo)
            self.blockIndex += 1
            self.blockInfoList.append(blockInfo)
            print(blockInfo.toString())

    def getBlockDetail(self, htmlClassInfo, blockInfo):
        htmlBlockTitle = htmlClassInfo.find("div", {"class" : "title"})
        titleObj = htmlBlockTitle.find("a", {"href" : re.compile("http://bj.lianjia.com/xiaoqu/*")})
        if titleObj == None:
            blockInfo.blockName = "无"
        else:
            blockInfo.blockName = titleObj.get_text()

        htmlBlockDealInfo = htmlClassInfo.find("div", {"class" : "houseInfo"})
        childObj = htmlBlockDealInfo.find("a", {"href" : re.compile("http*://bj.lianjia.com/chengjiao/*")})
        if childObj != None:
            blockInfo.blockDealUrl = childObj.get("href")

        htmlBlockPosition = htmlClassInfo.find("div", {"class" : "positionInfo"})
        districtObj = htmlBlockPosition.find("a", {"class" : "district"})
        if districtObj != None:
            blockInfo.blockPosition = districtObj.get_text()
        bizcircleObj = htmlBlockPosition.find("a", {"class" : "bizcircle"})
        if bizcircleObj != None:
            blockInfo.blockBusiCircle = bizcircleObj.get_text()

        htmlBlockTagList = htmlClassInfo.find("div", {"class" : "tagList"})
        if htmlBlockTagList != None:
            blockInfo.blockTag = htmlBlockTagList.get_text()

    # house
    def getDealHouseInfo(self, bsObj, blockInfo):
        htmlDealHouseInfoList = bsObj.findAll("div", {"class" : "info"})

        self.houseIndex = 0
        for htmlDealHouseInfo in htmlDealHouseInfoList:
            houseInfo = HouseInfo(blockInfo)
            houseInfo.houseIndex = self.houseIndex
            self.getDealHouseTitle(htmlDealHouseInfo, houseInfo)
            self.getDealDetaillInfo(htmlDealHouseInfo, houseInfo)
            self.houseInfoList.append(houseInfo)
            self.houseIndex += 1
            print(houseInfo.toString())
            self.saveIncrementFile(self.file, houseInfo)

    def getDealHouseTitle(self, htmlDealHouseInfo, houseInfo):
        htmlDealHouseTitle = htmlDealHouseInfo.find("div", {"class" : "title"})
        titleObj = htmlDealHouseTitle.find("a", {"href" : re.compile("http*://bj.lianjia.com/chengjiao/*")})
        houseInfo.houseName = titleObj.get_text()
        houseInfo.houseDealUrl = titleObj.get("href")

    def getDealDetaillInfo(self, htmlDealHouseInfo, houseInfo):
        htmlDealDate = htmlDealHouseInfo.find("div", {"class" : "dealDate"})
        houseInfo.dealDate = htmlDealDate.get_text()

        htmlTotalPrice = htmlDealHouseInfo.find("div", {"class" : "totalPrice"})
        totalPrice = htmlTotalPrice.get_text()
        houseInfo.totalPrice = totalPrice

        htmlPositionInfo = htmlDealHouseInfo.find("div", {"class" : "positionInfo"})
        positionInfo = htmlPositionInfo.get_text()
        houseInfo.positionInfo = positionInfo

        htmlUnitPriceInfo = htmlDealHouseInfo.find("div", {"class" : "unitPrice"})
        unitPrice = htmlUnitPriceInfo.get_text()
        houseInfo.unitPrice = unitPrice

        htmlDealHouseTxt = htmlDealHouseInfo.find("div", {"class", "dealHouseInfo"})
        if htmlDealHouseTxt == None:
            dealHouseTime = "未知"
        else:
            dealHouseTime = htmlDealHouseTxt.get_text()
        houseInfo.dealHouseTime = dealHouseTime

        htmlDealCycleTime = htmlDealHouseInfo.find("div", {"class", "dealCycleeInfo"})
        if htmlDealCycleTime == None:
            dealCycleTime = "未知"
        else:
            dealCycleTime = htmlDealCycleTime.get_text()
        houseInfo.dealCycleTime = dealCycleTime

    def printInfoList(self):
        for houseInfo in self.houseInfoList:
            print(houseInfo.toString())

    def saveHouseInfo(self):
        f = open("house_deal_list.csv", "wt")
        f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format("小区ID","小区","房子ID","房子名称","交易日期","总价","单价","位置","是否满五年","挂牌价和成交周期","房子详情链接","小区交易链接"))
        f.write("\n")
        for houseInfo in self.houseInfoList:
            f.write(houseInfo.toString())
            f.write("\n")
        f.close()

    def createIncrementFile(self):
        f = open("house_deal_list_increment.csv", "wt")
        f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}".format("小区ID","小区","房子ID","房子名称","交易日期","总价","单价","位置","是否满五年","挂牌价和成交周期","房子详情链接","小区交易链接"))
        f.write("\n")
        return f

    def saveIncrementFile(self, f,  houseInfo):
        f.write(houseInfo.toString())
        f.write("\n")


'''
test
'''

scrapyTest = ScrapyTest()
scrapyTest.beginScrapyBlock()
scrapyTest.beginScrapyHouse()
scrapyTest.saveHouseInfo()


