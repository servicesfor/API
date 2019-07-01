import random

from dao import BaseDao
from logger import api_logger

class MedicineDao(BaseDao):

    def find_illness(self):     #列表详情
        #查询疾病id和name
        sql = 'select id as ill_id ,ill_name  from yl_diseases'
        data = self.query(sql)
        return data

    def medicine_list(self,ill_id):     #药品列表显示

        data = self.find_illness()      #查询疾病信息
        if not data:
            return data == []
        for i in data:
            if i.get('ill_id') == ill_id:
                ill_name = i['ill_name']

        sql = ''

