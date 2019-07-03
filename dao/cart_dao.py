

from dao import BaseDao

class CartDao(BaseDao):

    def add_carts(self,c_user_id,c_med_id):       #添加购物车记录函数
        #查询该用户购物车中该药品的数量
        sql1 = "select c_med_num,c_med_id from carts " \
               "where c_user_id=%s and c_med_id=%s"
        #更新用户购物车中药品的数量，在原来的基础上增加1
        sql2 = "update carts set c_med_num=%s where c_user_id=%s and c_med_id=%s"
        #如果该用户购物车中没有该商品，则在购物车中添加一件该药品
        sql3 = "insert into carts(c_user_id,c_med_id,c_med_num,c_is_select)" \
               "values(%s,%s,1,True)"
        sql4 = "select count(*) as med_kind from carts " \
               "where c_user_id=%s "
        data = self.query(sql1,c_user_id,c_med_id)     #查询该用户购物车中该药品的数量
        if data:        #判断是否有记录
            num = data[0]['c_med_num'] + 1  #给当前数量加1
            self.query(sql2,num,c_user_id,c_med_id)
            data1 = self.query(sql1,c_user_id,c_med_id)
            data1.append(self.query(sql4,c_user_id)[0])
            return  data1   #返回更新后的药品数量
        data2 = self.query(sql3, c_user_id, c_med_id)
        data2.append(self.query(sql4, c_user_id)[0])
        return   data2     #添加药品，返回数量为1

    def sub_carts(self,user_id,med_id):       #删除购物车记录
        # 查询该用户购物车中该药品的数量
        sql1 = "select c_med_num,c_med_id " \
               "from carts where c_user_id=%s and c_med_id=%s"
        # 更新用户购物车中药品的数量，在原来的基础上增加1
        sql2 = "update carts set c_med_num=%s " \
               "where c_user_id=%s and c_med_id=%s"
        # 如果该用户购物车中没有该商品，则在购物车中添加一件该药品
        sql3 = "delete from carts " \
               "where c_user_id=%s and c_med_id=%s"
        sql4 = "select count(*) as med_kind from carts " \
               "where c_user_id=%s "
        data = self.query(sql1,user_id,med_id)       #查询购物车中数量
        num = data[0]['c_med_num'] - 1      #更新购物车中数量
        print(num,'=======num')
        if num > 0:                                 #
            self.query(sql2, num,user_id,med_id)     #更新购物车中的数量，减1
            data = self.query(sql1, user_id,med_id)
            data1 = self.query(sql4, user_id)
            if data1:
                data.append(data1[0])
                return data
            return []

        elif num == 0 :
            data1 = self.query(sql4, user_id)
            if data1:
                return data1
            return self.query(sql3,user_id,med_id)
        return self.query(sql3,user_id,med_id)       #清空该药品在购物车中的数据，返回空数组


