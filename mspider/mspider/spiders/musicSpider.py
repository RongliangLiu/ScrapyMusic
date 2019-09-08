# -*- coding: utf-8 -*-
from typing import List
import scrapy
import re
from mspider.items import MspiderItem

class MusicspiderSpider(scrapy.Spider):
    name = 'musicSpider'  # 爬虫识别名称
    allowed_domains = ['htqyy.com/']  # 爬取网页范围
    start_urls = ['http://www.htqyy.com/top/musicList/hot?pageIndex=0&pageSize=20']  # 起始网页

    def parse(self, response):
        # filename = "music.html"
        data = response.body.decode()  # 获取响应内容
        # open(filename, "wb").write(data)   # 写入到本地
        items = []  # 存放音乐信息的列表
        titles = re.findall(r'target="play" title="(.*?)"', data)  # 获取所有歌曲名
        artists = re.findall(r'target="_blank">(.*?)</a>', data)  # 获取所有艺术家

        for i in range(0, len(titles)):
            item = MspiderItem()
            item["title"] = titles[i]
            item["artist"] = artists[i]

        #     items.append(item)
        # return items
            yield item

            # 1、获取当前请求的url，提取页码信息
            beforeurl = response.url
            pat1 = r"pageIndex=(\d)"
            page = re.search(pat1, beforeurl).group(1)
            page = int(page) + 1  # 得到下一次请求的pageIndex

            # 2、构造下一页的url,发送下一次请求
            if page < 5:
                # 构造下一页url
                nexturl = "http://www.htqyy.com/top/musicList/hot?pageIndex="+str(page)+"&pageSize=20"
                # 发送下一次请求
                # 在parse方法里发送请求，并且这个请求完成后会继续调用parse
                yield scrapy.Request(nexturl, callback=self.parse)

