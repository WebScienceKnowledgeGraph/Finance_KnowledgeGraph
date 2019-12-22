import requests
from bs4 import BeautifulSoup
import csv
import datetime


class spiderHu(object):
    def __init__(self):
        self.headers = {
            "Cookie": "PHPSESSID=vb5ndj8l7locdgglkelhk8l2s0",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        self.url = "http://ipo.qichacha.com/c/{}"
        self.company = []
        self.stock = []
        self.industry = []
        self.legal_person = []
        self.chief = []
        self.area = []
        self.law_office = []
        self.share_holder = []
        self.leader = []

    @staticmethod
    def creat_table_stock(stock):
        headers = ['stock_id', 'stock_name', 'stock_price']
        with open('stock.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(stock)

    @staticmethod
    def creat_table_industry(industry):
        headers = ['stock_id', 'industry_name']
        with open('industry.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(industry)

    @staticmethod
    def creat_table_legal_person(legal_person):
        headers = ['stock_id', 'legal_person_name']
        with open('legal_person.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(legal_person)

    @staticmethod
    def creat_table_chief(chief):
        headers = ['stock_id', 'chief_name']
        with open('chief.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(chief)

    @staticmethod
    def creat_table_area(area):
        headers = ['stock_id', 'area_name']
        with open('area.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(area)

    @staticmethod
    def creat_table_law_office(law_office):
        headers = ['stock_id', 'law_office_name']
        with open('law_office.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(law_office)

    @staticmethod
    def creat_table_holder_company(holder_company):
        headers = ['stock_id', 'share_holder_company']
        temp = []

        for holder in holder_company:
            # print(holder)
            one = holder['stock_id']
            two = holder['share_holder_company']
            for t in two:
                holder_company_dict = {'stock_id': one, 'share_holder_company': t}
                temp.append(holder_company_dict)

        with open('holder_company.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(temp)

    @staticmethod
    def creat_table_leader(leader):
        headers = ['stock_id', 'leader_name']
        temp = []
        for l in leader:
            one = l['stock_id']
            two = l['leader_name']
            for t in two:
                leader_dict = {'stock_id': one, 'leader_name': t}
                temp.append(leader_dict)
        with open('leader.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(temp)

    @staticmethod
    def get_stock_id_lists():
        stock_id_lists = []
        with open('上交所.txt', 'r', encoding='utf-16') as f:
            headers = f.readline()
            line = f.readline()
            while line:
                data = line.strip().split('\t')
                stock_id_lists.append(data[2])
                line = f.readline()
        with open('深交所.txt', 'r', encoding='utf-16') as f:
            headers = f.readline()
            line = f.readline()
            while line:
                data = line.strip().split('\t')
                stock_id_lists.append(data[5])
                line = f.readline()
        return stock_id_lists

    def get_url_lists(self, stock_id_lists):
        url_lists = map(lambda stock_id: self.url.format(stock_id), stock_id_lists)
        return url_lists

    def parse_detail_url(self, url):
        # url_fuck = "http://ipo.qichacha.com/c/600733"
        response = requests.get(url=url, headers=self.headers)
        text = response.content.decode()
        soup = BeautifulSoup(text, 'html5lib')
        panel_body = soup.find_all('div', class_='panel-body')
        base_info = panel_body[0]
        tds_base_info = base_info.find_all('td')
        company = {}
        for index, td in enumerate(tds_base_info):
            # print(str(index) + str(list(td.stripped_strings)))

            temp = list(td.stripped_strings)
            if len(temp) == 0:
                continue
            temp = temp[0]
            if index == 1:
                company_name = temp
                company['company_name'] = company_name
            elif index == 7:
                stock_id = temp
                company['stock_id'] = stock_id
            elif index == 9:
                stock_name = temp
                company['stock_name'] = stock_name
            elif index == 21:
                industry_name = temp
                company['industry_name'] = industry_name
            elif index == 25:
                legal_person_name = temp
                company['legal_person_name'] = legal_person_name
            elif index == 29:
                chief_name = temp
                company['chief_name'] = chief_name
            elif index == 47:
                area_name = temp
                company['area_name'] = area_name
            elif index == 59:
                law_office_name = temp
                company['law_office_name'] = law_office_name
        # print(company)

        release_info = panel_body[1]
        tds_release_info = release_info.find_all('td')
        stock_price = list(tds_release_info[11].stripped_strings)[0]
        company['stock_price'] = stock_price

        gudong_info = panel_body[2]
        table_gudong_info = gudong_info.find_all('table', class_='table table-bordered')[0]
        trs = table_gudong_info.find_all('tr')
        share_holder_company = []
        for index, td in enumerate(trs):
            if index >= 1:
                share_holder_company.append(list(td.stripped_strings)[0])

        company['share_holder'] = share_holder_company

        manager_info = panel_body[3]
        table_manager_info = manager_info.find_all('table', class_='table table-bordered')[0]
        trs = table_manager_info.find_all('tr')
        manager = []
        for index, td in enumerate(trs):
            # 直接打印出股东列表
            if index >= 1:
                manager.append(list(td.stripped_strings)[0])
        # print(manager)

        # information about a company
        company['leader'] = manager
        self.company.append(company)



        stock = {
            'stock_id': company['stock_id'],
            'stock_name': company['stock_name'],
            'stock_price': company['stock_price']
        }
        self.stock.append(stock)
        industry = {
            'stock_id': company['stock_id'],
            'industry_name': company['industry_name']
        }
        self.industry.append(industry)
        legal_person = {
            'stock_id': company['stock_id'],
            'legal_person_name': company['legal_person_name']
        }
        self.legal_person.append(legal_person)
        chief = {
            'stock_id': company['stock_id'],
            'chief_name': company['chief_name']
        }
        self.chief.append(chief)
        area = {
            'stock_id': company['stock_id'],
            'area_name': company['area_name']
        }
        self.area.append(area)
        law_office = {
            'stock_id': company['stock_id'],
            'law_office_name': company['law_office_name']
        }
        self.law_office.append(law_office)
        share_holder_ = {
            'stock_id': company['stock_id'],
            'share_holder_company': company['share_holder']  # 这是一个列表

        }
        self.share_holder.append(share_holder_)
        leader_ = {
            'stock_id': company['stock_id'],
            'leader_name': company['leader']  # 这是一个列表
        }
        self.leader.append(leader_)
        # print(self.share_holder)
        # print(self.leader)
        # print(company)
        print(company['stock_id'])

    # 在此函数下调用写入文件函数
    def parse_url(self, url_lists):
        for index, url in enumerate(url_lists):
            self.parse_detail_url(url)

    @staticmethod
    def load_in_csv(companies):
        headers = ['company_name', 'stock_id', 'stock_name', 'industry_name', 'legal_person_name', 'chief_name',
                   'area_name', 'law_office_name', 'stock_price', 'share_holder', 'leader']
        with open('company.csv', 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(companies)

    def spider(self):
        # 获取股票代码
        stock_id_lists = self.get_stock_id_lists()

        # 根据股票代码生成相应的url，爬去url所对应的界面
        url_lists = self.get_url_lists(stock_id_lists)
        self.parse_url(url_lists)

        # 写成csv文件
        self.creat_table_stock(self.stock)
        self.creat_table_industry(self.industry)
        self.creat_table_legal_person(self.legal_person)
        self.creat_table_chief(self.chief)
        self.creat_table_area(self.area)
        self.creat_table_law_office(self.law_office)
        self.creat_table_holder_company(self.share_holder)
        self.creat_table_leader(self.leader)
        self.load_in_csv(self.company)

    def run(self):
        self.spider()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    spider = spiderHu()
    spider.run()
    end_time = datetime.datetime.now()
    print('程序运行' + str(end_time - start_time))
