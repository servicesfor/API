from flask import url_for

from dao import BaseDao
from logger import api_logger


class DoctorDao(BaseDao):  # 问医生dao
    def find_ofc(self, ofc_list):  # 查科室dao
        ofc_data = {}  # 创建科室数据字典
        ofcs_list = []
        ofcs = []  # 创建小科室列表
        # 查询科室数据库
        sql = 'select * from departments ' \
              'where id=%s'
        # 小科室分类名称
        title = ['常见科室', '内科', '外科', '其他']
        for i in range(len(ofc_list)):
            for j in ofc_list[i]:
                ofc = self.query(sql, j)

                if i == 0:
                    # 添加常见科室图标
                    ofc[0]['img'] = url_for('static', filename="ofc_img/" + str(j) + ".png")
                ofcs.append(ofc[0])  # 汇总科室分类
            ofc_data["title"] = title[i]
            ofc_data['departments_info'] = ofcs
            ofcs_list.append(ofc_data)
            ofcs = []
            ofc_data = {}

        return ofcs_list

    def find_doct(self, depid):  # 查询医生列表

        # 查询医生id,name,照片,科室名称,职称,擅长方向
        sql1 = """
                select doc.id,doc.doc_name ,dep.name,doc.doc_img,doc_title,doc_goods
                from doctors as doc inner join departments as dep 
                on doc.department_id=dep.id 
                and dep.id=%s;
                """
        # 查询医院名称
        sql2 = """
                select hop.hosp_name
                from doctors as doc inner join hospitals as hop 
                on doc.hospital_id=hop.id   
                and doc.id=%s ;
                """
        # 查询医生星级,月回答次数,月处方数,回复时间,是否力荐,图文价格,电话问诊价格
        sql3 = """
                select d_level,m_answer,m_recipel,avg_response,is_recommend,text_price,tel_price
                from doctors as doc inner join doctor_quality as qua 
                on qua.d_name_id=doc.id   
                and doc.id=%s ;
                """
        data = self.query(sql1, depid)  # 查询科室id对应的医生列表

        for i in range(len(data)):
            doct_id = data[i]['id']  # 遍历每个医生的id

            data1 = self.query(sql2, doct_id)  # 查询每个医生所属医院
            data2 = self.query(sql3, doct_id)  # 查询每个医生的详细信息
            data[i]["avg_response"] = data2[0]['avg_response']  # 回复时间
            data[i]["d_level"] = data2[0]['d_level']  # 医生星级
            data[i]["is_recommend"] = data2[0]['is_recommend']  # 是否力荐
            data[i]["m_answer"] = data2[0]['m_answer']  # 月回答次数
            data[i]["m_recipel"] = data2[0]['m_recipel']  # 月处方数
            data[i]["tel_price"] = data2[0]['tel_price']  # 电话问诊费用
            data[i]["text_price"] = data2[0]['text_price']  # 图文问诊费用
            if data1:
                # 所属医院
                data[i]["hop_name"] = data1[0]['hosp_name']
            else:
                data[i]["hop_name"] = ''

        return data

    def doct_resume(self, id):  # 医生履历

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

        data = self.query(sql1, id)  # 通过医生表查询医院     医院名，地址，电话，医保，等级
        for i in range(len(data)):
            # 查询通过医生表查询科室表  医生名，医生图片，职称，擅长，简历，科室名
            data1 = self.query(sql2, id)
            # 通过医生查询医生详情表   是否力荐
            data2 = self.query(sql3, id)
            if data1:
                s = data1[0]['is_recommend']  # 从列表中提取是否力荐
                data[i]["is_recommend"] = s
                # 在data[i]字典中添加is_recommend键
            else:
                data[i]["is_recommend"] = ''
                # 如果没有力荐,则添加空字符串为value
            if data2:
                # 将医院详情提取出来加入到data中
                data.append(data2[0])
            else:
                data.append([])
        return data

    def doctor_detail(self, id):  # 医生详情页面
        doct_dic = {}
        sql1 = '''
        select doc.doc_name,doc_img,doc_title,doc_exp,doc.id as doc_id,qua.m_answer,d_level,avg_response,
        is_recommend,text_price,tel_price from doctor_quality as qua inner join doctors 
        as doc on doc.id=qua.d_name_id and doc.id=%s;
        '''  # 医生表，医生相关属性表查询医生名、头像、职称、从业时间、月回答、医生等级、平均响应、是否力荐、图文问诊、电话问诊
        sql2 = '''
        select dep.name as dep_name from departments as dep 
        inner join doctors as doc on doc.department_id=dep.id and doc.id=%s;
        '''  # 医生表，科室表查询医生科室名
        sql3 = '''
        select hos.hosp_name,hosp_level from hospitals as hos 
        inner join doctors as doc on doc.hospital_id and doc.id=%s;
        '''  # 医生表，医院表查询医院名、医院等级
        sql4 = '''
        select adv.anonymous,adv_con,comm_time from user_adv_info as adv 
        inner join doctors as doc on adv.doc_id=doc.id and doc.id=%s;      
         '''  # 医生表，咨询表查询用户匿名、咨询信息、咨询时间
        data = self.query(sql1, id)
        data1 = self.query(sql2, id)
        data2 = self.query(sql3, id)
        data3 = self.query(sql4, id)
        doct_dic["doc_det_info"] = data[0]
        if data1:
            doct_dic["doc_info"] = data1[0]
        else:
            doct_dic["doc_info"] = ''
        if data2:
            doct_dic["doc_dep"] = data2[0]
        else:
            doct_dic["doc_dep"] = ''

        if data3:
            doct_dic["user_comm"] = data3
        else:
            doct_dic["user_comm"] = ''

        return doct_dic
