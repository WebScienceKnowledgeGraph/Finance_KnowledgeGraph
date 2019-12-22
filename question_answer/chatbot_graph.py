#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_answer.question_classifier import *
from question_answer.question_parser import *
from question_answer.answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        # 问题分类模板
        self.classifier = QuestionClassifier()
        # 问题分类模板 -> sql语句
        self.parser = QuestionPaser()
        # sql语句 -> 回答模板
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是小雨金融智能助理，希望可以帮到您。如果没答上来，可多关照。祝您身体棒棒！'
        # 寻找提问问题的对应的分类模板
        res_classify = self.classifier.classify(sent)
        # 如果找不到对应的分类模板，返回固定回复
        if not res_classify:
            return answer
        # 如果找到对应的分类模板，再将其转换为sql语句
        res_sql = self.parser.parser_main(res_classify)
        # 根据此sql语句返回相应的回答模板
        final_answers = self.searcher.search_main(res_sql)
        # 如果没有相应的回答模板，返回固定回复
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小雨:', answer)

