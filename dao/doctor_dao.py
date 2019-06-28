from flask import url_for

from dao import BaseDao
from logger import api_logger

class DoctorDao(BaseDao):   #问医生dao
    def find_ofc(self,ofc_list):     #查科室dao
        ofc_data = {}           #创建科室数据字典
        ofcs = []                  #创建小科室列表
        #查询科室数据库
        sql = 'select * from departments ' \
              'where id=%s'
        keys = ["common_ofc","nei_ofc","wai_ofc","other_ofc"]   #小科室分类名称
        for i in range(len(ofc_list)):
            for j in ofc_list[i]:
                ofc = self.query(sql,j)[0] # 获取用户表中的用户id和口令
                if i == 0:
                    #添加常见科室图标
                    ofc['img'] = url_for('static',filename="ofc_img/" + str(j) + ".png")
                ofcs.append(ofc)   #汇总科室分类
            ofc_data[keys[i]] = ofcs
            ofcs = []
        return ofc_data

    def find_doct(self,id):         #查询医生列表
        doct_dict = {}
        #查询医生id,name,照片,
        sql1 = """
        select doc.id,doc.doc_name ,dep.name,doc.doc_img,doc_title,doc_goods
    from doctors as doc inner join departments as dep on doc.department_id=dep.id 
    and dep.id=%s;
        """

        sql2 = """
                select hop.hosp_name
            from doctors as doc inner join hospitals as hop on doc.hospital_id=hop.id   
            and doc.id=%s;
                """

        sql3 = """
            select d_level,m_answer,m_recipel,avg_response,is_recommend,text_price,tel_price
            from doctors as doc inner join doctor_quality as qua on qua.d_name_id=doc.id   
            and doc.id=%s;
        """
        data = self.query(sql1, id)

        for i in range(len(data)):
            doct_id = data[i]['id']

            data1 = self.query(sql2, doct_id)
            data2 = self.query(sql3,doct_id)[0]
            data[i]["d_level"] = data2
            if data1:
                s = data1[0]['hosp_name']
                data[i]["hop_name"] = s
            else:
                data[i]["hop_name"] = ''

            doct_dict[doct_id] = data[i]


        return doct_dict

    def doct_detail(self, id):  # 医生履历
        doct_dict = {}
        sql1 = '''               
        select doc.doc_name,doc_img,doc_title,doc_goods,doc_resume,dep.name as dep_name 
        from doctors as doc inner join departments as dep on doc.department_id=dep.id 
        and doc.id=%s;
        '''  # 查询通过医生表查询科室表  医生名，医生图片，职称，擅长，简历，科室名
        sql2 = '''
        select doctor_quality.is_recommend 
        from doctors inner join doctor_quality on doctor_quality.d_name_id=doctors.id 
        and doctors.id=%s;
        '''  # 通过医生查询医生详情表   是否力荐
        sql3 = '''
        select hos.hosp_name,hosp_addr,hosp_tel,medical_insurance,hosp_level 
        from hospitals as hos inner join doctors on doctors.hospital_id=hos.id 
        and doctors.id=%s;
        '''  # 通过医生表查询医院     医院名，地址，电话，医保，等级

        data = self.query(sql1, id)     # 通过医生表查询医院     医院名，地址，电话，医保，等级
        for i in range(len(data)):
            # 查询通过医生表查询科室表  医生名，医生图片，职称，擅长，简历，科室名
            data1 = self.query(sql2, id)
            # 通过医生查询医生详情表   是否力荐
            data2 = self.query(sql3, id)
            if data1:
                s = data1[0]['is_recommend']        #从列表中提取是否力荐
                data[i]["is_recommend"] = s
                #在data[i]字典中添加is_recommend键
            else:
                data[i]["is_recommend"] = ''
                #如果没有力荐,则添加空字符串为value
            if data2:
                s = data2[0]    #将医院详情提取出来加入到data中
                data[i]['hosp_detail'] = s
            else:
                data[i]['hosp_detail'] = ''

            doct_dict[id] = data[i]

        return doct_dict







