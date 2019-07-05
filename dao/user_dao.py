from dao import BaseDao
from libs.sms import new_code
from logger import api_logger

from libs.crypt import check_password


class UserDao(BaseDao):
    def find_userid(self, phone):
        return self.query("select id as user_id " \
                          "from yl_user where phone=%s", phone)[0]["user_id"]

    def save(self, **values):
        api_logger.info('db insert yl_user: <%s>' % values['phone'])

        return super(UserDao, self).save('yl_user', **values)

    def check_login_name(self, phone):
        # 检查用户名是否已存在
        result = self.query('select id  from yl_user where phone=%s', phone)
        return bool(result)  # 已存在返回True

    def login_str(self, phone, login_auth_str):
        user_data = self.login_data(phone)  # 获取用户表中的用户id和口令
        if user_data:
            user_id, auth_str = (user_data[0].get('id'),
                                 user_data[0].get('login_auth_str'))

            if check_password(login_auth_str, auth_str):
                # 验证成功
                return True
            # api_logger.warn('用户 %s 的口令不正确' % phone)
            return False

    def login_data(self, phone):
        sql = 'select * from yl_user ' \
              'where phone=%s and activated=%s '
        user_data = self.query(sql, phone, 1)  # 获取用户表中的用户id和口令
        return user_data

    def focus_doc(self, user_id):
        sql = 'select count(*) as my_focus from focus_doc where user_id=%s'
        return self.query(sql, user_id)[0]["my_focus"]

    def patient_list(self, user_id):  # 患者列表
        sql = '''SELECT id,p_name,p_sex,(YEAR(CURDATE()) - YEAR(date_birth)) as age,p_weight from patient where p_user_id=%s;
        '''
        return self.query(sql, user_id)

    def update_name(self, nick_name, userid):  # 更改用户昵称
        sql1 = "UPDATE yl_user SET nick_name='%s'" % nick_name + " WHERE id = '%s'" % (userid);
        sql2 = "update yl_user set update_time=now() where id =%s" % (userid)
        self.query(sql1)
        self.query(sql2)

    def return_own_mes(self, u_id):  # 查询个人页面
        content = {}
        # 查询收藏内容总数
        sql1 = "select count(*) from doc_adv where u_name_id=%s"
        # 我的问诊我的处方
        sql2 = "select count(*) from orders where o_user_id=%s"  # 药品订单
        sql3 = "select count(*) from focus_doc where user_id=%s"  # 关注医生
        sql4 = "select count(*) from collect_art where user_id=%s"
        sql5 = "select photo,nick_name from yl_user where id=%s"  # 查询昵称 头像

        content["nick_name"] = self.query(sql5, u_id)[0]["nick_name"]
        content["photo"] = self.query(sql5, u_id)[0]["photo"]
        content["focus_doctor"] = self.query(sql3, u_id)[0]["count(*)"]
        content["collect_content"] = self.query(sql4, u_id)[0]["count(*)"]
        content["my_inquiry"] = self.query(sql2, u_id)[0]["count(*)"]
        content["my_recipel"] = self.query(sql1, u_id)[0]["count(*)"]
        return content

    def focus_doctors(self, doc_id, u_id):  # 关注医生功能

        sql = "select * from focus_doc where doc_id=%s and user_id=%s"
        if self.query(sql, doc_id, u_id):
            self.query("delete from focus_doc where doc_id=%s " \
                       "and user_id=%s ", doc_id, u_id)
        self.query("insert into focus_doc(doc_id,user_id) " \
                   "values(%s,%s)", doc_id, u_id)

    def setting_page(self, user_id):  # 查询昵称头像电话和性别
        sql = "select nick_name,photo,sex,phone from yl_user where id=%s"
        return self.query(sql, user_id)

    def collect_art(self, art_id, u_id):
        sql = "select * from collect_art where doc_id=%s and user_id=%s"
        if self.query(sql, art_id, u_id):
            self.query("delete from collect_art where art_id=%s " \
                       "and user_id=%s ", art_id, u_id)
        self.query("insert into collect_art(art_id,user_id) " \
                   "values(%s,%s)", art_id, u_id)

    def update_phone(self, phone):
        sql1 = 'select phone from yl_user where phone=%s;'
        data1 = self.query(sql1, phone)
        if data1:
            return '该手机号已存在！'
        new_code(phone)  # 发送验证码
        return "发送验证码成功!"

    def update_Verifi(self, phone, user_id):
        sql1 = "update yl_user set phone='%s' where id=%s;" % (phone, user_id)
        self.query(sql1)
        return

    def collect_article(self, u_id):
        sql1 = "select arc_id from collect_art where user_id='%s'" % (u_id)
        sql2 = "select id as act_id,title,auth,auth_img " \
               "from articles where id=%s"
        data = self.query(sql1)
        if not data:
            return "暂无收藏"
        arc_ids = []
        for i in data:
            arc_ids.append(i["arc_id"])
        for i in arc_ids:
            data = self.query(sql2, i)
        return data

    def my_focus(self, u_id):
        sql1 = "select doc_id from focus_doc where user_id=%s"
        sql2 = '''               
                select doc.doc_name,doc_img,doc_title,doc_goods,dep.name as dep_name 
                from doctors as doc inner join departments as dep on doc.department_id=dep.id 
                and doc.id=%s;
                '''  # 查询通过医生表查询科室表  医生名，医生图片，职称，擅长，简历，科室名
        sql3 = '''
                select qua.d_level,qua.m_answer,qua.avg_response
                from doctors as doc inner join doctor_quality as qua 
                on qua.d_name_id=doc.id 
                and doc.id=%s;
                '''  # 通过医生查询医生详情表   是否力荐
        sql4 = '''
                select hos.hosp_name
                from hospitals as hos inner join doctors on doctors.hospital_id=hos.id 
                and doctors.id=%s;
                '''  # 通过医生表查询医院     医院名，地址，电话，医保，等级

        data = self.query(sql1, u_id)
        if not data:
            return "暂无关注"
        doc_ids = []
        my_focus = []
        for i in data:
            doc_ids.append(i["doc_id"])
        for i in doc_ids:
            data = self.query(sql2, i)[0]
            data["hosp_name"] = self.query(sql4, i)[0]["hosp_name"]
            data["d_level"] = self.query(sql3, i)[0]["d_level"]
            data["m_answer"] = self.query(sql3, i)[0]["m_answer"]
            data["avg_response"] = self.query(sql3, i)[0]["avg_response"]
            my_focus.append(data)

        return my_focus

    def forget_pwd(self, phone):
        sql = 'select phone from yl_user where phone=%s;'
        if not self.query(sql, phone):
            return '该手机号不存在！'
        new_code(phone)  # 发送验证码
        return "发送验证码成功!"

    def new_password(self, auth_str, user_id):
        self.query("update yl_user set login_auth_str=%s where id=%s")

    def is_exist(self, phone):  # 注册判断手机号是否已存在
        sql = 'select * from yl_user where phone=%s '
        data = self.query(sql, phone)
        return data