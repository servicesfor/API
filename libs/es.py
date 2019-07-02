"""
封装ElasticSearch搜索引擎的SDK(library库)
"""
import requests
from pymysql.cursors import DictCursor
import pymysql


class ESearch():
    def __init__(self,index):
        self.host = '121.199.63.71'
        self.port = '9206'
        self.index = index

    def create_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        # ES基于json数据进行交互的，所以上传数据必须是json格式的数据
        # resp是请求响应对象， 通过resp.json()获取响应的json数据
        resp = requests.put(url,json={
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            }
        })
        resp_data = resp.json()
        #print(resp_data)
        if resp_data.get('acknowledged'):
            print('create index %s ok!' % self.index)

    def add_doc(self,doc_type,id=None,**values):
        url = f'http://{self.host}:{self.port}/{self.index}/{doc_type}/'
        if id:
            url += f"{id}"
        resp = requests.post(url,json=values)
        resp_data = resp.json()
        #print(resp_data)
        if resp_data.get('result') == "created":
            print('add doc %s ok!' % values)
        else:
            print('add doc %s error!' % values)

    def query(self,keyword):
         url = f'http://{self.host}:{self.port}/{self.index}/_search?q={keyword}'
         resp = requests.get(url)
         resp_data = resp.json()
         if resp_data.get('hits').get('total') > 0:
             return {
                 'code':200,
                 'total':resp_data.get('hits').get('total'),
                 'datas': [data.get('_source')
                           for data in resp_data.get('hits').get('hits')]
             }
         else:
             return {'code':201,'msg':'无'}

def init_index():

    # 连接数据库，将doctors表数据添加到索引库中
    db =  pymysql.Connect(host="121.199.63.71",
                         port=3306,
                         user='yladmin',
                         password='yl123',
                         db='yl_api_db',charset='utf8')
    with db.cursor(cursor=DictCursor) as c:
        #c.execute('select doc_name, doc_title, doc_exp from doctors')
        #c.execute('select name,price,drug_stock from drugs ')
        #c.execute('select hosp_name,hosp_addr,hosp_tel,hosp_level from hospitals ')
        #c.execute('select name from departments ')
        c.execute('select ill_name,symptom,pathogeny,treatment,diagnosis,Prevention,life from yl_diseases ')
        #es_ = ESearch('ylindex')
        #es_ = ESearch('drugindex')
        #es_ = ESearch('hospindex')
        #es_ = ESearch('depindex')
        es_ = ESearch('diseaseindex')
        es_.create_index()
        for row_data in c.fetchall():
        #for row_data in c.fetchmany(10):
            #print(row_data)
            #es_.add_doc('doctor',**row_data)
            #es_.add_doc('drug', **row_data)
            #es_.add_doc('hospital', **row_data)
            es_.add_doc('diseases', **row_data)
        print('--init add doctor doc_type all ok--')

if __name__ == '__main__':
    #init_index()
    #search = ESearch('ylindex')
    #search = ESearch('drugindex')
    #search = ESearch('hospindex')
    search = ESearch('diseaseindex')
    print(search.query('头疼'))
