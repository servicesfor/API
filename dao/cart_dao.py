from flask import url_for

from dao import BaseDao

class CartDao(BaseDao):

    def add_carts(self,**values):       #添加购物车记录函数
        #查询该用户购物车中该药品的数量
        sql1 = "select c_med_num " \        
              "from carts where c_user_id=%(user_id)s and med_id=%(med_id)s"
        #更新用户购物车中药品的数量，在原来的基础上增加1
        sql2 = "update carts set c_med_num=%s where c_user_id=%(user_id)s and med_id=%(med_id)s"
        #如果该用户购物车中没有该商品，则在购物车中添加一件该药品
        sql3 = "insert into carts(c_user_id,c_med_id,c_med_num,c_is_select) "\
                "values(%(user_id)s,%(med_id)s,1,True)"
        data = self.query(sql1,**values)     #查询该用户购物车中该药品的数量
        if data:        #判断是否有记录
            num = data[0]['c_med_num'] + 1  #给当前数量加1
            self.query(sql2,num,**values)
            return  self.query(sql1,**values)   #返回更新后的药品数量
        return self.query(sql3,**values)        #添加药品，返回数量为1

    def sub_carts(self,**values):       #删除购物车记录
        # 查询该用户购物车中该药品的数量
        sql1 = "select c_med_num " \
               "from carts where c_user_id=%(user_id)s and med_id=%(med_id)s"
        # 更新用户购物车中药品的数量，在原来的基础上增加1
        sql2 = "update carts set c_med_num=%s where c_user_id=%(user_id)s and med_id=%(med_id)s"
        # 如果该用户购物车中没有该商品，则在购物车中添加一件该药品
        sql3 = "delete from carts where c_user_id=%(user_id)s and med_id=%(med_id)s"
        data = self.query(sql1, **values)       #查询购物车中数量
        num = data[0]['c_med_num'] - 1      #更新购物车中数量
        if num > 0:                                 #
            self.query(sql2, num, **values)     #更新购物车中的数量，减1
            return self.query(sql1, **values)   #返回更新后的数量
        return self.query(sql3, **values)       #清空该药品在购物车中的数据，返回空数组


