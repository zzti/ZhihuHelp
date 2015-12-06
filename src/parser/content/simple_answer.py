# -*- coding: utf-8 -*-
import copy
from src.lib.bs4 import BeautifulSoup
from src.parser.content.answer import Answer
from src.tools.debug import Debug


class SimpleAnswer(Answer):
    def set_dom(self, dom):
        self.info = {}
        if dom and not (dom.select('div.answer-status')):
            self.header = dom.find('div', class_='zm-item-vote-info')
            self.body = dom.find('textarea', class_='content')
            self.footer = dom.find('div', class_='zm-meta-panel')
            if self.body:
                self.content = BeautifulSoup(self.get_tag_content(self.body), 'html.parser')
            self.author_parser.set_dom(dom)
        return

    def parse_answer_content(self):
        # 移除无用的span元素
        if not self.content:
            Debug.logger.debug(u'答案内容未找到')
            return
        content = copy.deepcopy(self.content)
        span = content.find('span', class_='answer-date-link-wrap')
        if not span:
            Debug.logger.debug(u'答案内容未找到')
            return
        span.extract()
        self.info['content'] = self.get_tag_content(content)
        return

    def parse_date_info(self):
        if not self.content:
            Debug.logger.debug(u'答案更新日期未找到')
            return
        data_block = self.content.find('a', class_='answer-date-link')
        if not data_block:
            Debug.logger.debug(u'答案更新日期未找到')
            return
        commit_date = self.get_attr(data_block, 'data-tip')
        if commit_date:
            update_date = data_block.get_text()
            self.info['edit_date'] = self.parse_date(update_date)
            self.info['commit_date'] = self.parse_date(commit_date)
        else:
            commit_date = data_block.get_text()
            self.info['edit_date'] = self.info['commit_date'] = self.parse_date(commit_date)

    def parse_href_info(self):
        if not self.content:
            Debug.logger.debug(u'答案更新日期未找到')
            return
        href_tag = self.content.find('a', class_='answer-date-link')
        if not href_tag:
            Debug.logger.debug(u'问题id，答案id未找到')
            return
        href = self.get_attr(href_tag, 'href')
        self.parse_question_id(href)
        self.parse_answer_id(href)
        self.info['href'] = "http://www.zhihu.com/question/{question_id}/answer/{answer_id}".format(**self.info)
        return
