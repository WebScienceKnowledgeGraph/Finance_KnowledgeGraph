#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args'] #1.(词典)问句关键词和所对应类型
        entity_dict = self.build_entitydict(args) #改成了词典{关键词的类型1：【关键词1，关键词2...],...}
        question_types = res_classify['question_types'] #list:问句类型
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'company_location':
                sql = self.sql_transfer(question_type, entity_dict.get('company'))

            elif question_type == 'company_industry':
                sql = self.sql_transfer(question_type, entity_dict.get('company'))

            elif question_type == 'company_chief':
                sql = self.sql_transfer(question_type, entity_dict.get('company'))

            elif question_type == 'company_stock':
                sql = self.sql_transfer(question_type, entity_dict.get('company'))

            elif question_type == 'stockname_ID':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'stockname_price':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'stockname_company':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'stockname_shareholder':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'area_countcompany':
                sql = self.sql_transfer(question_type, entity_dict.get('area'))

            elif question_type == 'industry_countcompany':
                sql = self.sql_transfer(question_type, entity_dict.get('industry'))

            elif question_type == 'chief_company':
                sql = self.sql_transfer(question_type, entity_dict.get('chief'))

            elif question_type == 'legalperson_company':
                sql = self.sql_transfer(question_type, entity_dict.get('legal_person'))

            elif question_type == 'ID_name':
                sql = self.sql_transfer(question_type, entity_dict.get('stockID'))

            elif question_type == 'ID_price':
                sql = self.sql_transfer(question_type, entity_dict.get('stockID'))

            elif question_type == 'company_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('company'))

            elif question_type == 'stock_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            # elif question_type == 'disease_easyget':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            #
            # elif question_type == 'disease_desc':
            #     sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls #list:(词典1：{问句类型1：对应的sql语句}，词典2：{问句类型2：对应的sql语句})

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询公司的所在地
        if question_type == 'company_location':
            sql = ["MATCH (m:Company) where m.name = '{0}' return m.name,m.area".format(i) for i in entities]

        # 查询公司的所属行业
        elif question_type == 'company_industry':
            sql = ["MATCH (m:Company) where m.name = '{0}' return m.name,m.industry".format(i) for i in entities]

        # 查询公司的董事
        elif question_type == 'company_chief':
            sql = ["MATCH (m:Company) where m.name = '{0}' return m.name,m.chief".format(i) for i in entities]

        # 查询公司的股票
        elif question_type == 'company_stock':
            sql = ["MATCH (m:Company) where m.name = '{0}' return m.name,m.stock".format(i) for i in entities]

        # ！查询股票的价格
        elif question_type == 'stockname_price':
            sql = ["MATCH (m:Company) where m.stock = '{0}' return m.stock,m.stock_price".format(i) for i in entities]

        # 查询发行股票的公司
        elif question_type == 'stockname_company':
            sql = ["MATCH (m:Company) where m.stock = '{0}' return m.stock,m.name".format(i) for i in entities]

        # 查询股票的大股东
        elif question_type == 'stockname_shareholder':
            sql = ["MATCH (m:Company)-[:has_holder_company]->(n:Share_holder) where m.stock = '{0}' return m.stock,n.name".format(i) for i in entities]

        #！已知地区查所在地区公司总量
        elif question_type == 'area_countcompany':
            sql = ["MATCH (m:Company) where m.area = '{0}' return m.area,count(m)".format(i) for i in entities]

        # 已知行业查所在行业公司总量
        elif question_type == 'industry_countcompany':
            sql = ["MATCH (m:Company) where m.industry = '{0}' return m.industry,count(m)".format(i) for i in entities]

        # 已知董事求公司名
        elif question_type == 'chief_company':
            sql = ["MATCH (m:Company) where m.chief = '{0}' return m.chief,m.name".format(i) for i in entities]

        # 已知法人求公司名
        elif question_type == 'legalperson_company':
            sql = ["MATCH (m:Company) where m.legal_person = '{0}' return m.legal_person,m.name".format(i) for i in entities]

        elif question_type == 'company_desc':
            sql = ["MATCH (m:Company) where m.name = '{0}' return m.name,m.chief, m.industry, m.stock, m.stock_price".format(i) for i in entities]

        elif question_type == 'stock_desc':
            sql = ["MATCH (m:Company) where m.stock = '{0}' return m.stock,m.chief, m.industry, m.name, m.stock_price".format(i) for i in entities]
        # elif question_type == 'symptom_disease':
        #     sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询某地的公司总量
        # elif question_type == 'area_countcompany':
        #     sql = ["MATCH (m:Company)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        #
        #
        # # 查询疾病的并发症
        # elif question_type == 'disease_acompany':
        #     sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        # # 查询疾病的忌口
        # elif question_type == 'disease_not_food':
        #     sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 查询疾病建议吃的东西
        # elif question_type == 'disease_do_food':
        #     sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 已知忌口查疾病
        # elif question_type == 'food_not_disease':
        #     sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 已知推荐查疾病
        # elif question_type == 'food_do_disease':
        #     sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 查询疾病常用药品－药品别名记得扩充
        # elif question_type == 'disease_drug':
        #     sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 已知药品查询能够治疗的疾病
        # elif question_type == 'drug_disease':
        #     sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        # # 查询疾病应该进行的检查
        # elif question_type == 'disease_check':
        #     sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 已知检查查询疾病
        # elif question_type == 'check_disease':
        #     sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
