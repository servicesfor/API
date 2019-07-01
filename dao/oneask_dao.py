
from dao import BaseDao

class OneAskDao(BaseDao):
    def oneask_list(self, id):  # 一元问医生
        doct_dis = {}
        sql1 = '''
           select id,dep.name from departments as dep;
           '''  # 查询部门id、名称

        sql2 = '''
           select doc.id from departments as dep inner join doctors as doc on doc.department_id=dep.id and dep.id=%s;
           '''  # 医生id、姓名、职称、擅长、部门
        sql3 = '''
           select qua.d_level,m_answer,text_price,discount,dis_num,new_excl,d_name_id from  doctor_quality as qua inner join doctors as doc on doc.id=qua.d_name_id where (qua.discount is not null) and doc.id=%s;
           '''  # 医生星级、月回答次数、折后图文咨询费用、折扣、剩余名额、是否新人专享
        sql4 = '''
                   select dep.name,doc.id,doc_name,doc_title,doc_goods from departments as dep inner join doctors as doc on doc.department_id=dep.id and doc.id=%s;
                   '''  # 医生id、姓名、职称、擅长、部门

        list1,list2,list3,list4,list5 = [],[],[],[],[]
        data3 = {}
        data1 = self.query(sql1)
        data2 = self.query(sql2, id)
        if not data2:
            return
        for i in range(len(data2)):
            list1.append(data2[i]['id'])

        for id in list1:
            if self.query(sql3, id):
                list2.append(self.query(sql3, id)[0])
                list3.append(self.query(sql3, id)[0]['d_name_id'])
        for id in list3:
            list4.append(self.query(sql4,id)[0])
        for i in range(len(list4)):
            data3["doctor"] = list4[i]
            data3["doctor_details"] = list2[i]
            list5.append(data3)

        doct_dis['department'] = data1
        doct_dis['doctor'] = list5

        return doct_dis
