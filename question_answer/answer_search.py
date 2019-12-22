from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            "bolt://localhost:7687",
            username="neo4j",
            password="chenhuan")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        # 最终回答
        final_answers = []
        # 传过来的sql语句
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            # 查询条件
            for query in queries:
                # 单个条件查询结果
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        # {'args': {'TCL集团股份有限公司': ['company']}, 'question_types': ['company_location']}
        if question_type == 'company_location':
            desc = [i['m.area'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的位置在{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 查询公司的所属行业
        elif question_type == 'company_industry':
            desc = [i['m.industry'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}所在行业是{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 查询公司的董事
        elif question_type == 'company_chief':
            desc = [i['m.chief'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的董事是{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 查询公司的股票
        elif question_type == 'company_stock':
            desc = [i['m.stock'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的发行的股票是{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # ！查询股票的价格
        elif question_type == 'stockname_price':
            desc = answers[0]['m.stock_price']
            subject = answers[0]['m.stock']
            final_answer = '{0}的股价是{1}'.format(subject, desc)

        # 查询发行股票的公司
        elif question_type == 'stockname_company':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.stock']
            final_answer = '{0}这只股票的发行公司是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 查询股票的大股东
        elif question_type == 'stockname_shareholder':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.stock']
            final_answer = '{0}的大股东是{1}'.format(subject, '、'.join(list(set(desc))[:self.num_limit]))

        # ！已知地区查所在地区公司总量
        elif question_type == 'area_countcompany':
            desc = answers[0]['count(m)']
            subject = answers[0]['m.area']
            final_answer = '{0}地区内公司总量是{1}'.format(subject, desc)

        # ！已知行业查所在行业公司总量
        elif question_type == 'industry_countcompany':
            desc = answers[0]['count(m)']
            subject = answers[0]['m.industry']
            final_answer = '{0}行业内公司总量是{1}'.format(subject, desc)

        # 已知董事求公司名
        elif question_type == 'chief_company':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.chief']
            final_answer = '{0}是{1}的董事'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 已知法人求公司名
        elif question_type == 'legalperson_company':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.legal_person']
            final_answer = '{0}担保的公司是{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 已知公司求公司简介：董事，行业，股票，股票价格
        elif question_type == 'company_desc':
            chief = answers[0]['m.chief']
            industry = answers[0]['m.industry']
            stock = answers[0]['m.stock']
            stock_price = answers[0]['m.stock_price']
            subject = answers[0]['m.name']
            final_answer = '{0}的董事是{1},属于{2}行业，股票是{3},股票价格是{4}'.format(subject,chief,industry,stock,stock_price)

        # 已知股票求股票简介：董事，行业，公司名称，股票价格
        elif question_type == 'stock_desc':
            chief = answers[0]['m.chief']
            industry = answers[0]['m.industry']
            stock = answers[0]['m.stock']
            stock_price = answers[0]['m.stock_price']
            subject = answers[0]['m.stock']
            final_answer = '{0}的董事是{1},属于{2}行业，股票是{3},股票价格是{4}'.format(subject, chief, industry, stock, stock_price)

        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
