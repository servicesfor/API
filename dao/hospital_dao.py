from dao import BaseDao

class HospitalDao(BaseDao):
    def hosp_detail(self,id):  # 医院详情
        hosp,id1,list1 = [],[],[]
        dict1 = {}

        sql1 = '''
        select doc.id,hosp.id,hosp_name,hosp_addr,hosp_tel,medical_insurance,hosp_level from hospitals as hosp inner join doctors as doc on doc.hospital_id=hosp.id and hosp.id=%s;
        '''     # 查询医院id、医院名称、医院地址、医院电话、医保、医院等级
        sql2 = '''
        select doc.id,doc_name,doc_title,doc_goods from doctors as doc inner join hospitals as hosp on doc.hospital_id=hosp.id and doc.id=%s; 
        ''' # 查询医生id、医生姓名、医生职称、医生擅长
        sql3 = '''
        select doc.id,qua.d_level,m_answer,avg_response,text_price,tel_price,is_recommend from doctor_quality as qua inner join doctors as doc on qua.d_name_id=doc.id and doc.id=%s;
        '''     # 查询医生星级、月回答次数、响应时间、电话问诊、图文问诊
        sql4 = '''
        select dep.name from departments as dep inner join doctors as doc on dep.id=doc.department_id and doc.id=%s;
        '''     # 查询医生所属科室

        data1 = self.query(sql1,id)
        if  not data1:
            return
        dict1['hosp'] = data1[0]
        for i in range(len(data1)):
            id1.append(data1[i]['id'])      #将所属医院的所有医生id添加到id1列表中
        for j in range(len(id1)):
            data2 = self.query(sql2,id1[j])[0]   #将医生详情加入list1列表中
            data2['d_level']=self.query(sql3,id1[j])[0]['d_level']
            data2['m_answer']=self.query(sql3,id1[j])[0]['m_answer']
            data2['avg_response'] = self.query(sql3,id1[j])[0]['avg_response']
            data2['text_price'] = self.query(sql3,id1[j])[0]['text_price']
            data2['tel_price'] = self.query(sql3,id1[j])[0]['tel_price']
            data2['is_recommend'] = self.query(sql3,id1[j])[0]['is_recommend']
            data2['name'] = self.query(sql4,id1[j])[0]['name']
            hosp.append(data2)
        dict1['doctors'] =hosp
        return dict1
