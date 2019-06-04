import json
from urllib.parse import urljoin

import scrapy

from LiQu.items import LiquItem


class LiQuSpider(scrapy.Spider):
    name = "LiQu"
    start_urls = [
        "https://www.liqucn.com/rj/",
        "https://www.liqucn.com/yx/",
    ]

    def parse(self, response):
        # print("查看获取的响应：", response.text)
        # 该页的数据---> 列表存储
        datas = response.xpath('//ul[@class="tip_blist"]/li/div[@class="tip_list"]/span')
        # 页号的最后一个标签
        page_last = response.xpath('//div[@class="page"]/a[last()]/text()').extract_first()
        # 当前请求的url
        curr_url = response.url
        for data in datas:
            # 创建字典
            dd = dict()
            # APP 名称
            app_name = data.xpath('./a/text()').extract_first()
            # APP 详情页链接
            app_url = data.xpath('./a/@href').extract_first()
            # 向字典中添加值
            dd['app_name'] = app_name
            dd['app_url'] = app_url
            # 记录到文件中
            self.record(dd)
            # 请求详情页
            yield scrapy.Request(url=app_url, callback=self.parse_detail)
        # 判断最后一个标签的文本值
        if page_last == "尾页":
            # 获取倒数第二个的属性
            next_url = response.xpath('//div[@class="page"]/a[last()-1]/@href').extract_first()
            # 判断当前的url 中是否包含 ?page
            if "?page" in curr_url:
                # 说明这不是首页
                url = curr_url.split('?')[0] + next_url
                # 发起下一页的请求
                yield scrapy.Request(url=url, callback=self.parse)
            url = urljoin(curr_url, next_url)
            yield scrapy.Request(url=url, callback=self.parse)
        if page_last == "下一页":
            # 获取其属性
            next_url = response.xpath('//div[@class="page"]/a[last()]/@href').extract_first()
            # 判断当前的url 中是否包含 ?page
            if "?page" in curr_url:
                # 说明这不是首页
                url = curr_url.split('?')[0] + next_url
                # 发起下一页的请求
                yield scrapy.Request(url=url, callback=self.parse)
            url = urljoin(curr_url, next_url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        """
        解析详情页数据
        :param response:
        :return:
        """
        # 创建item
        item = LiquItem()
        # print("查看获取的详情页数据：", response.text)
        # APP 名称
        app_name = response.xpath('//div[@class="info_con"]/h1/text()').extract_first()
        # APP 详情介绍
        # 获取第一个p标签的 title 内容
        title_1 = response.xpath('//div[@class="info_con"]/p[1]/text()').extract()
        text_1 = response.xpath('//div[@class="info_con"]/p[1]/em/text()').extract()
        # 获取第二个p标签的title内容
        title_2 = response.xpath('//div[@class="info_con"]/p[2]/text()').extract()
        text_2 = response.xpath('//div[@class="info_con"]/p[2]/em/text()').extract()
        # 合并两个列表
        title = title_1 + title_2
        text = text_1 + text_2
        # 将两个列表打包成字典
        app_info = dict(zip(title, text))
        item['app_name'] = app_name
        item['app_info'] = app_info
        yield item

    def record(self, data):
        """
        将二级分类的列表信息写入文件:字典转json
        :param data:
        :return:
        """
        with open(r'G:\工作\APP\LiQu\LiQu_info.json', 'a+', encoding="utf-8") as f:
            # 将字典的数据转为json
            result = json.dumps(data, ensure_ascii=False)
            # 将结果写入文件
            f.write(result + "\n")
