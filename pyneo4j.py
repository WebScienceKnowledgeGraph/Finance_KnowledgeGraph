#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node

class FinanceGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('\\')[:-1])
        self.data_path = '/'.join(os.path.join(cur_dir, 'data/company.json').split('\\'))
        self.g = Graph(
            "bolt://localhost:7687",
            username="neo4j",
            password="chenhuan")

    '''1.读取文件'''
    def read_nodes(self):
        # 实体
        companies = []
        stocks = []
        industries = []
        legal_persons = []
        chiefs = []
        areas = []
        law_offices = []
        share_holders = []
        leaders = []

        company_infos = []

        # 实体关系
        rels_stocks = []
        rels_industry = []
        rels_legal_person = []
        rels_chief = []
        rels_area = []
        rels_law_office = []
        rels_share_holder = []
        rels_leader = []

        f = open(self.data_path,encoding='UTF-8')
        dict = json.load((f))
        for data_json in dict:
            company_dict = {}
            company = data_json['company_name']
            company_dict['company'] = company
            companies.append(company)
            company_dict['stock'] = ''
            company_dict['industry'] = ''
            company_dict['legal_person'] = ''
            company_dict['chief'] = ''
            company_dict['area'] = ''
            company_dict['law_office'] = ''
            company_dict['stock_price'] = ''

            if 'stock_name' in data_json:
                stock = data_json['stock_name']
                company_dict['stock'] = stock
                stocks.append(stock)
                rels_stocks.append([company,stock])

            if 'industry_name' in data_json:
                industry = data_json['industry_name']
                company_dict['industry'] = industry
                industries.append(industry)
                rels_industry.append([company,industry])

            if 'legal_person_name' in data_json:
                legal_person = data_json['legal_person_name']
                company_dict['legal_person'] = legal_person
                legal_persons.append(legal_person)
                rels_legal_person.append([company,legal_person])

            if 'chief_name' in data_json:
                chief = data_json['chief_name']
                company_dict['chief'] = chief
                chiefs.append(chief)
                rels_chief.append([company,chief])

            if 'area_name' in data_json:
                area = data_json['area_name']
                company_dict['area'] = area
                areas.append(area)
                rels_area.append([company,area])

            if 'law_office_name' in data_json:
                law_office = data_json['law_office_name']
                company_dict['law_office'] = law_office
                law_offices.append(law_office)
                rels_law_office.append([company,law_office])

            if 'stock_price' in data_json:
                company_dict["stock_price"] = data_json['stock_price']

            if 'share_holder' in data_json:
                share_holder_str = data_json['share_holder']
                share_holder_json = eval(share_holder_str)
                for _share_holder in share_holder_json:
                    share_holders.append(_share_holder)
                    rels_share_holder.append([company, _share_holder])

            if 'leader' in data_json:
                leader_str = data_json['leader']
                leader_json = eval(leader_str)
                for _leader in leader_json:
                    leaders.append(_leader)
                    rels_leader.append([company, _leader])

            company_infos.append(company_dict)

        return set(companies),set(stocks),set(industries),set(legal_persons),set(chiefs),set(areas),set(law_offices),set(share_holders),set(leaders),\
               company_infos,\
               rels_stocks,rels_industry,rels_legal_person,rels_chief,rels_area,rels_law_office,rels_share_holder,rels_leader

    '''3.建立节点'''
    def create_node(self, label, nodes):
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
        return

    '''2.创建知识图谱中心Stock的节点'''
    def create_company_nodes(self, company_infos):
        for company_dict in company_infos:
            node = Node("Company", name=company_dict['company'], stock=company_dict['stock'],
                        industry=company_dict['industry'] ,legal_person=company_dict['legal_person'],
                        chief=company_dict['chief'],area=company_dict['area'],
                        law_office=company_dict['law_office'],
                        stock_price=company_dict['stock_price'])
            self.g.create(node)

        return

    '''4.创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Companies,Stocks,Industries,Legal_persons,Chiefs,Areas,Law_offices,Share_holders,Leaders, \
        company_infos, \
        rels_stock, rels_industry, rels_legal_person, rels_chief, rels_area, rels_law_office, rels_share_holder, rels_leader\
        = self.read_nodes()

        self.create_company_nodes(company_infos)
        self.create_node('Stock', Stocks)
        self.create_node('Industry', Industries)
        self.create_node('Legal_person', Legal_persons)
        self.create_node('Chief', Chiefs)
        self.create_node('Area', Areas)
        self.create_node('Law_office', Law_offices)
        self.create_node('Share_holder', Share_holders)
        self.create_node('Leader', Leaders)

        return


    '''6.创建实体关系边'''
    def create_graphrels(self):
        Companies, Stocks, Industries, Legal_persons, Chiefs, Areas, Law_offices, Share_holders, Leaders, \
        company_infos, \
        rels_stock, rels_industry, rels_legal_person, rels_chief, rels_area, rels_law_office, rels_share_holder, rels_leader \
            = self.read_nodes()
        self.create_relationship('Company', 'Stock', rels_stock, 'has_stock', '股票')
        self.create_relationship('Company', 'Industry', rels_industry, 'belongs_to', '所属行业')
        self.create_relationship('Company', 'Legal_person', rels_legal_person, 'has_legal_person', '法人')
        self.create_relationship('Company', 'Chief', rels_chief, 'has_chief', '董事')
        self.create_relationship('Company', 'Area', rels_area, 'belongs_to', '所属区域')
        self.create_relationship('Company', 'Law_office', rels_law_office, 'has_law_office', '法务办公室')
        self.create_relationship('Company', 'Share_holder', rels_share_holder, 'has_holder_company', '持股公司')
        self.create_relationship('Company', 'Leader', rels_leader, 'has_leader', '领事')


    '''5.建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
            except Exception as e:
                print(e)
        return

if __name__ == '__main__':
    handler = FinanceGraph()
    handler.create_graphnodes()
    handler.create_graphrels()