from dao import BaseDao


class ReceiveDao(BaseDao):
    def add_receive(self,user_id,rec_name,rec_phone,rec_addr):
        sql1 = "insert into yl_receive(r_user_id,r_name,r_phone,r_addr,r_default)" \
              " values(%s,%s,%s,%s,%s )"
        sql2 = "select * from yl_receive where r_user_id=%s"

        r_default = False
        #查询该用户是否已有收货地址,如果有,则直接插入,不设为默认地址,如果没有,则设为默认地址
        if self.query(sql2,user_id):
            self.query(sql1,user_id,rec_name,rec_phone,rec_addr,r_default)
        else:
            self.query(sql1,user_id,rec_name,rec_phone,rec_addr,not r_default)

    def del_receive(self,user_id,r_id):
        #删除选中的收货信息
        sql1 = "delete from  yl_receive where id=%s"

        sql2 = "update yl_receive set r_default=%s " \
               "where r_user_id=%s"
        sql3 = "select * from yl_receive where id=%s"
        sql4 = "select * from yl_receive where r_user_id=%s"

        if len(self.query(sql4,user_id)) ==1:   #如果用户只有一条数据,则直接删除
            self.query(sql1,r_id)
        elif len(self.query(sql4,user_id)) == 2:    #如果用户有两条记录,则删除之后将另一条设为默认地址
            self.query(sql1, r_id)
            self.query(sql2,True,user_id)
        # 如果超过两条数据 ,则判断该条记录是不是默认地址,如果是,则直接删除,并设置第一条记录为默认地址,如果不是,则直接删除
        elif self.query(sql3,r_id)[0]['r_default']:
            self.query(sql1, r_id)
            self.query("update yl_receive set r_default=TRUE " \
               "where r_user_id=%s limit 1",user_id)
        self.query(sql1, r_id)

    def change_default(self,r_id):

        if self.query("select r_default from yl_receive where id=%s",r_id)[0]["r_default"]:

            print(self.query("select r_default from yl_receive where id=%s",r_id)[0])
            return
        default_id = self.query("select id from yl_receive where r_default=True ")[0]["id"]

        self.query("update yl_receive set r_default=FALSE " \
                   "where id=%s", default_id)
        self.query("update yl_receive set r_default=TRUE " \
                   "where id=%s", r_id)

    def find_receive(self,r_id):
        return self.query("select id as r_id,r_name,r_phone,r_addr "
                   "from yl_receive where id=%s ",r_id)[0]

    def edit_receive(self,r_name,r_phone,r_addr,r_id):
        sql = "update yl_receive set r_name=%s,r_phone=%s,r_addr=%s where id=%s"
        self.query(sql,r_name,r_phone,r_addr,r_id)



