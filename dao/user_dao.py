import datetime

from dao import BaseDao
from logger import api_logger

from libs.crypt import make_password, check_password


class UserDao(BaseDao):

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

    def focus_doctors(self, user_id):
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


if __name__ == '__main__':
    values = {}

    values['create_time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(values)
