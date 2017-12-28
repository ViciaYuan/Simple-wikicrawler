import scrapy
from scrapy import Request,Selector
from ..items import entryItem

import re

class wikicrawler_2(scrapy.Spider):
    name = "wikicrawler_2"
    start_urls = ["https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95"]
    host = "http://zh.wikipedia.org"
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        content = selector.xpath("//div[@class=\"mw-parser-output\"]//tr//td//a")
        for categories in content:
            names = categories.xpath("string(.)").extract_first()
            url = self.host + categories.xpath("@href").extract_first()
            yield Request(url=url, callback=self.parse_pages)

    def parse_pages(self,response):
        selector = Selector(response)
        content = selector.xpath("//div[@id=\"mw-pages\"]//ul//li//a")
        for page in content:
            names = page.xpath("string(.)").extract_first()
            url = self.host + page.xpath("@href").extract_first()
            yield Request(url=url, callback=self.parse_entry)
        sub_cate = selector.xpath("//div[@id=\"mw-subcategories\"]//ul//li//a")
        for category in sub_cate:
            subcate = category.xpath("string(.)").extract_first()
            cateurl = self.host + category.xpath("@href").extract_first()
            yield Request(url=cateurl, callback=self.parse_pages)


    def parse_entry(self, response):
        selector = Selector(response)

        # 词条url
        url = response.url

        # 词条名称name
        name_node = selector.xpath("//h1")
        name = name_node.xpath("string(.)").extract_first()

        # 词条信息
        info_node = selector.xpath("//div[@id='toc']/preceding-sibling::p")
        info = ""
        for infor in info_node:
            info += "\n" + infor.xpath("string(.)").extract_first()

        # 词条目录及内容content，以字典存储
        content_node = selector.xpath("//div[@id='toc']//li//span[@class='toctext']")
        content_list = []
        for title in content_node:
            content_name = title.xpath("string(.)").extract_first()
            content_list.append(content_name)
        content = dict.fromkeys(tuple(content_list))
        keys = list(content.keys())
        for i, key in enumerate(keys):

            # 对上一次循环中多余的内容进行删减
            if i > 0:
                topic_clears = selector.xpath("//span[@id=\"" + key + "\"]/../preceding-sibling::p| \
                                               //span[@id=\"" + key + "\"]/../preceding-sibling::div| \
                                               //span[@id=\"" + key + "\"]/../preceding-sibling::ul| \
                                               //span[@id=\"" + key + "\"]/../preceding-sibling::table")
                topic_clearlist = []
                for topic_clear in topic_clears:
                    topic_clearlist.append(topic_clear.xpath('string(.)').extract_first())
                source_list = content[keys[i - 1]]
                content[keys[i - 1]] = [a for a in topic_clearlist if a in source_list]

            topics = selector.xpath("//span[@id=\"" + key + "\"]/../following-sibling::p| \
                                    //span[@id=\"" + key + "\"]/../following-sibling::div| \
                                    //span[@id=\"" + key + "\"]/../following-sibling::ul| \
                                    //span[@id=\"" + key + "\"]/../following-sibling::table")
            topic_contend = []
            for topic in topics:
                topic_contend.append(topic.xpath('string(.)').extract_first())
            content[key] = topic_contend

        # 简介
        summary = []
        summ = selector.xpath("//span[@id=\"简介\"]/../following-sibling::p")
        if '简介' in content:
            summary = content['简介']
        elif summ:
            for sum in summ:
                summary.append(sum.xpath('string(.)').extract_first())
        else:
            summary = []

        # 更新时间uptime
        uptime_node = selector.xpath("//li[@id='footer-info-lastmod']")
        uptime_sentence = uptime_node.xpath("string(.)").extract_first()
        uptime = re.findall(r'(?<!\d)\d*:?\d+(?!\d)', uptime_sentence, flags=0)
        uptime = uptime[0] + '.' + uptime[1] + '.' + uptime[2] + ' ' + uptime[3]

        # 参考资料refer，以列表存储
        refer_node = selector.xpath("//span[@id='参考文献']/../following-sibling::div//ol[@class='references']/li")
        refer = []
        for references in refer_node:
            refer.append(references.xpath("string(.)").extract_first())

        # 词条标签label，即其分类，以列表存储
        label_node = selector.xpath("//div[@id='mw-normal-catlinks']/ul/li")
        label = []
        for labels in label_node:
            label.append(labels.xpath("string(.)").extract_first())

        item = entryItem()
        item["url"] = url
        item["name"] = name
        item["summary"] = summary
        item["info"] = info
        item["content"] = content
        item["uptime"] = uptime
        item["refer"] = refer
        item["label"] = label
        yield item


