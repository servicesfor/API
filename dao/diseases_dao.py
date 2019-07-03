from dao import BaseDao


class DiseaseDao(BaseDao):
    def query_diseases(self):
        sql = '''
        SELECT id,ill_name from yl_diseases WHERE 1 ORDER BY CONVERT( ill_name USING gbk ) COLLATE gbk_chinese_ci ASC 
        '''
        return self.query(sql)


    def diseases_message(self,dis_id):
        sql = '''
            SELECT id,ill_name,symptom,pathogeny,treatment,diagnosis,prevention,life from yl_diseases WHERE  id=%s
            '''
        return self.query(sql,dis_id)