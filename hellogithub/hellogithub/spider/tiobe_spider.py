#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/7/19 下午3:19
#   Desc    :   tiobe 语言排名
import datetime
import re
from decimal import *

from lxml import html, etree
from peewee import DoesNotExist

from base_spider import BaseSpider
from hellogithub.models.base import database
from hellogithub.models.tiobe import TiobeHall, TiobeRank, TiobeContent


class Tiobe(BaseSpider):
    spider_name = 'tiobe_spider'
    
    def __init__(self, rss_url, index_url):
        super(Tiobe, self).__init__()
        self.rss_url = rss_url
        self.index_url = index_url
        self.publish_date = None
    
    @property
    def today(self):
        return datetime.date.today()
    
    def check_content(self):
        """
        查看当月内容是否存在
        """
        try:
            content_obj = TiobeContent.select().order_by(TiobeContent.publish_date).get()
            return content_obj.publish_date.month == self.today.month
        except DoesNotExist:
            return False

    def check_publish(self):
        response_obj = self.get_data(self.rss_url)
        if not response_obj:
            self.logger.error(u'获取 rss url 数据失败')
            return None
        tree = etree.fromstring(response_obj.text)
        publish_date = tree.xpath('/rss/channel/item/pubDate/text()')
        # 时间格式：Wed, 02 Aug 2017 23:42:22
        if publish_date:
            publish_date = datetime.datetime.strptime(
                publish_date[0].strip(), "%a, %d %b %Y %H:%M:%S").date()
            self.publish_date = publish_date
            return publish_date <= self.today
        else:
            self.logger.warning(u'未解析到 rss 日期')
            return False

    def fetch(self, force=False):
        if self.check_content():
            self.logger.info(u'新数据未发布')
            return
        if self.check_publish() or force:
            self.logger.info(u'获取数据中...')
            response_obj = self.get_data(self.index_url)
            if response_obj:
                self.logger.info(u'解析数据中...')
                tree = html.fromstring(response_obj.text)
                rank_result, hall_result = self.parse_table(tree)
                chart_result = self.parse_chart(tree)
                title, description = self.parse_content(tree)

                if (self.save_content(title, description, chart_result) and
                    self.save_rank(rank_result) and self.save_hall(hall_result)):
                    self.logger.info(u'数据存储完成！')
                else:
                    self.logger.info(u'数据未更新')

            else:
                self.logger.error(u'获取 index url 数据失败')
        elif self.check_publish() is None:
            pass
        else:
            self.logger.info(u'新数据未发布')
            
    @staticmethod
    def percentage2int(input_str):
        # '12.7%' -> 12700
        return int(Decimal(input_str.strip()[:-1]).quantize(Decimal('0.000')) * 1000)

    def parse_rank(self, top20, next30):
        """
        解析并返回前五十编程语言评级表
        """
        rank_list = []
        positions_list = top20.xpath('./tbody/tr/td[1]/text()')
        languages_list = top20.xpath('./tbody/tr/td[4]/text()')
        ratings_list = top20.xpath('./tbody/tr/td[5]/text()')
        positions_list.extend(next30.xpath('./tbody/tr/td[1]/text()'))
        languages_list.extend(next30.xpath('./tbody/tr/td[2]/text()'))
        ratings_list.extend(next30.xpath('./tbody/tr/td[3]/text()'))
        for i, position in enumerate(positions_list):
            rank_list.append({'position': int(position),  # '1' -> 1
                              'language': languages_list[i].strip(),
                              'rating': ratings_list[i].strip(),
                              'rating_int': self.percentage2int(ratings_list[i]),
                              'publish_date': self.publish_date})
        return rank_list

    def parse_hall(self, hall_of_fame):
        """
        解析并返回年度语言表
        """
        hall_list = []
        # 该 table 没有 tbody 标签（前端的锅）
        year_list = hall_of_fame.xpath('./tr/td[1]/text()')
        winners_list = hall_of_fame.xpath('./tr/td[2]/text()')
        for i, year in enumerate(year_list):
            hall_list.append({'year': int(year),
                              'publish_date': self.publish_date,
                              'language': winners_list[i].strip()})
        return hall_list
    
    def parse_table(self, tree_element):
        """
        解析所有的表
        返回评级表、年度语言表
        """
        tables = tree_element.xpath('//table')
        top20_element, next30_element, history_element, hall_of_fame_element = \
            tables[0], tables[1], tables[2], tables[3]
        rank_result = self.parse_rank(top20_element, next30_element)
        hall_result = self.parse_hall(hall_of_fame_element)
        return rank_result, hall_result
    
    @staticmethod
    def parse_chart(tree_element):
        """
        解析并返回绘图需要的数据
        """
        javascript_str = tree_element.xpath('//article/script/text()')[1]
        pattern = re.compile(r'\{name.*')
        s = re.search(pattern, javascript_str)
        if s:
            series_str = s.group()
        else:
            series_str = ''
        return series_str
    
    @staticmethod
    def parse_content(tree_element):
        """
        解析并返回本期的描述和标题
        """
        title = tree_element.xpath('//article/h3[1]/text()')
        description = tree_element.xpath('//article/p[1]/text()')
        if title and description:
            return title[0], description[0].strip()
        else:
            return '' ''

    def save_rank(self, rank_data_list):
        count = 0
        for rank_data in rank_data_list:
            _, create_result = TiobeRank.get_or_create(**rank_data)
            if create_result:
                count += 1
        if count:
            self.logger.info(u'存储 rank 数据完成，共：{}'.format(count))
            return True

    def save_hall(self, hall_data_list):
        count = 0
        for hall_data in hall_data_list:
            _, create_result = TiobeHall.get_or_create(**hall_data)
            if create_result:
                count += 1
        if count:
            self.logger.info(u'存储 hall 数据完成，共：{}'.format(count))
            return True
        
    def save_content(self, title, description, chart):
        _, create_result = TiobeContent.get_or_create(
            title=title, description=description,
            publish_date=self.publish_date, chart_str=chart)
        if create_result:
            self.logger.info(u'存储 content 数据完成。')
            return True

if __name__ == '__main__':
    database.create_tables([TiobeContent, TiobeRank, TiobeHall], safe=True)

    RSS_URL = 'https://www.tiobe.com/tiobe-index/rss.xml'
    INDEX_URL = 'https://www.tiobe.com/tiobe-index/'
    
    t = Tiobe(RSS_URL, INDEX_URL)
    t.fetch()