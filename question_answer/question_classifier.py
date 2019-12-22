#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
#import ahocorasick
import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('\\')[:-2])
        #　特征词路径
        self.area_path = os.path.join(cur_dir, 'dict/area.txt')
        self.chief_path = os.path.join(cur_dir, 'dict/chief.txt')
        self.company_path = os.path.join(cur_dir, 'dict/company.txt')
        self.industry_path = os.path.join(cur_dir, 'dict/industry.txt')
       # self.leader_path = os.path.join(cur_dir, 'dict/leader.txt')
        self.legal_person_path = os.path.join(cur_dir, 'dict/legal_person.txt')
        self.stock_path = os.path.join(cur_dir, 'dict/stock.txt')
        self.stockID_path = os.path.join(cur_dir, 'dict/stock_id.txt')
        # 加载特征词,下面的这些wds就是把txt里面的都转成数组了
        # for i in open(self.area_path, encoding='UTF-8'):
             # i.strip()
        self.area_wds = [i.strip() for i in open(self.area_path, encoding='UTF-8') if i.strip()]
        self.chief_wds= [i.strip() for i in open(self.chief_path, encoding='UTF-8') if i.strip()]
        self.company_wds= [i.strip() for i in open(self.company_path) if i.strip()]
        self.industry_wds= [i.strip() for i in open(self.industry_path, encoding='UTF-8') if i.strip()]
        # self.leader_wds= [i.strip() for i in open(self.leader_path) if i.strip()]
        self.legal_person_wds= [i.strip() for i in open(self.legal_person_path) if i.strip()]
        self.stock_wds= [i.strip() for i in open(self.stock_path, encoding='UTF-8') if i.strip()]
        self.stockID_wds = [i.strip() for i in open(self.stockID_path) if i.strip()]
        self.region_words = set(self.area_wds + self.chief_wds + self.company_wds + self.industry_wds
                                # + self.leader_wds
                                + self.legal_person_wds + self.stock_wds + self.stockID_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))  #建成的树
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict() #用来给每一词来标上area,cheif,company,industry啥的标签
        # 问句疑问词
        self.location_qwds = ['在哪', '哪里', '地方', '地区', '地域', '地理位置']
        self.industrytype_qwds = ['干什么的', '行业', '领域', '类型']
        self.chief_qwds = ['董事', '老大']
        self.ID_qwds = ['ID', '编号', '编码', '号码','id']
        self.price_qwds = ['价格', '多少钱', '多贵','股价']
        self.stock_qwds = ['哪只股', '发行', '股票']
        self.shareholder_qwds = ['控股', '股东']
        self.count_qwds = ['多少', '数量','总量']
        self.company_qwds = ['公司', '企业', '集团', '哪家']
        self.name_qwds = ['股票', '名字', '是啥', '哪只股']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        finance_dict = self.check_finance(question)  #在问句中提取关键词词组，返回关键词组所对应的类型
        if not finance_dict:
            return {}
        data['args'] = finance_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in finance_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 公司在哪 company_location
        if self.check_words(self.location_qwds, question) and ('company' in types):
            question_type = 'company_location'
            question_types.append(question_type)
        # 公司所处行业 company_industry
        if self.check_words(self.industrytype_qwds, question) and ('company' in types):
            question_type = 'company_industry'
            question_types.append(question_type)
        # 公司董事 company_cheif
        if self.check_words(self.chief_qwds, question) and ('company' in types):
            question_type = 'company_chief'
            question_types.append(question_type)
        # 公司股票 company_stock
        if self.check_words(self.stock_qwds, question) and ('company' in types):
            question_type = 'company_stock'
            question_types.append(question_type)
        # 股票ID stockname_ID
        if self.check_words(self.ID_qwds, question) and ('stock' in types):
            question_type = 'stockname_ID'
            question_types.append(question_type)
        # 股票价格 stockname_price
        if self.check_words(self.price_qwds, question) and ('stock' in types):
            question_type = 'stockname_price'
            question_types.append(question_type)
        # 股票公司 stockname_company
        if self.check_words(self.company_qwds, question) and ('stock' in types):
            question_type = 'stockname_company'
            question_types.append(question_type)
        # 股票大股东 #stockname_shareholder
        if self.check_words(self.shareholder_qwds, question) and ('stock' in types):
            question_type = 'stockname_shareholder'
            question_types.append(question_type)
        # 某地多少家公司 area_countcompany
        if self.check_words(self.count_qwds, question) and ('area' in types):
            question_type = 'area_countcompany'
            question_types.append(question_type)
        # 行业多少家公司 industry_countcompany
        if self.check_words(self.count_qwds, question) and ('industry' in types):
            question_type = 'industry_countcompany'
            question_types.append(question_type)
        # 某人是哪家董事 chief_company
        if self.check_words(self.company_qwds, question) and ('chief' in types):
            question_type = 'chief_company'
            question_types.append(question_type)
        # 某人是哪家法人 legalperson_company
        if self.check_words(self.company_qwds, question) and ('legal_person' in types):
            question_type = 'legalperson_company'
            question_types.append(question_type)
        # 知股票ID问名字 ID_name
        if self.check_words(self.name_qwds, question) and ('stockID' in types):
            question_type = 'ID_name'
            question_types.append(question_type)
        # 知股票ID问价格 ID_price
        if self.check_words(self.price_qwds, question) and ('stockID' in types):
            question_type = 'ID_price'
            question_types.append(question_type)

        # # 推荐食品
        # if self.check_words(self.food_qwds, question) and 'disease' in types:
        #     deny_status = self.check_words(self.deny_words, question)
        #     if deny_status:
        #         question_type = 'disease_not_food'
        #     else:
        #         question_type = 'disease_do_food'
        #     question_types.append(question_type)
        #
        # #已知食物找疾病
        # if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
        #     deny_status = self.check_words(self.deny_words, question)
        #     if deny_status:
        #         question_type = 'food_not_disease'
        #     else:
        #         question_type = 'food_do_disease'
        #     question_types.append(question_type)
        #
        # # 推荐药品
        # if self.check_words(self.drug_qwds, question) and 'disease' in types:
        #     question_type = 'disease_drug'
        #     question_types.append(question_type)
        #
        # # 药品治啥病
        # if self.check_words(self.cure_qwds, question) and 'drug' in types:
        #     question_type = 'drug_disease'
        #     question_types.append(question_type)
        #
        # # 疾病接受检查项目
        # if self.check_words(self.check_qwds, question) and 'disease' in types:
        #     question_type = 'disease_check'
        #     question_types.append(question_type)
        #
        # # 已知检查项目查相应疾病
        # if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
        #     question_type = 'check_disease'
        #     question_types.append(question_type)
        #
        # #　症状防御
        # if self.check_words(self.prevent_qwds, question) and 'disease' in types:
        #     question_type = 'disease_prevent'
        #     question_types.append(question_type)
        #
        # # 疾病医疗周期
        # if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
        #     question_type = 'disease_lasttime'
        #     question_types.append(question_type)
        #
        # # 疾病治疗方式
        # if self.check_words(self.cureway_qwds, question) and 'disease' in types:
        #     question_type = 'disease_cureway'
        #     question_types.append(question_type)
        #
        # # 疾病治愈可能性
        # if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
        #     question_type = 'disease_cureprob'
        #     question_types.append(question_type)
        #
        # # 疾病易感染人群
        # if self.check_words(self.easyget_qwds, question) and 'disease' in types :
        #     question_type = 'disease_easyget'
        #     question_types.append(question_type)
        #
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        # if question_types == [] and 'disease' in types:
        #     question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该公司的描述信息返回
        if question_types == [] and 'company' in types:
            question_types = ['company_desc']
        # 若没有查到相关的外部查询信息，那么则将该股票的描述信息返回
        if question_types == [] and 'stock' in types:
            question_types = ['stock_desc']
        # # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        # if question_types == [] and 'symptom' in types:
        #     question_types = ['symptom_disease']
        #
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.area_wds:
                wd_dict[wd].append('area')
            if wd in self.chief_wds:
                wd_dict[wd].append('chief')
            if wd in self.company_wds:
                wd_dict[wd].append('company')
            if wd in self.industry_wds:
                wd_dict[wd].append('industry')
            if wd in self.legal_person_wds:
                wd_dict[wd].append('legal_person')
            if wd in self.stock_wds:
                wd_dict[wd].append('stock')
            if wd in self.stockID_wds:
                wd_dict[wd].append('stockID')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_finance(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)