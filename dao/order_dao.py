from dao import BaseDao
from datetime import datetime

from dao.cart_dao import CartDao

ORDER_STATUS_NOT_PAY = 0   # 待付款
ORDER_STATUS_NOT_SEND = 1   # 待发货
ORDER_STATUS_NOT_RECEIVE = 2  # 待收货
ORDER_STATUS_FINISHED = 3       #已完成

class OrderDao(BaseDao):

    def next_order_id(self):
        data = self.query('select max(o_id) as max_num from orders')
        if not data:
            data = "20190703"

        next_num = data[0].get('max_num')
        current_date = datetime.now().strftime('%Y%m%d')
        if next_num:
            last_date = next_num[:8]
            last_num = next_num[8:]
            if current_date == last_date:
                last_num = int(last_num)+1
                return "%s%s" % (last_date, str(last_num).rjust(5, '0'))

        return '%s00001' % current_date

    def create_order(self,user_id):
        #在order表中插入用户id,订单id,订单总价,订单状态,下单时间,默认收货地址
        sql1 = """
            insert into orders(o_user_id,o_price,o_id,o_status,o_time,o_receive_id)
            values (%s,%s,%s,%s,%s,%s)
        """
        sql3 = """
        insert into orders(o_user_id,o_price,o_id,o_status,o_time)
            values (%s,%s,%s,%s,%s)
        """
        #在order_details表中插入order_id,药品id
        sql2 = "insert into order_detail(o_order_id,o_goods_id,o_med_num,o_med_price) " \
              " values (%s,%s,%s,%s)"


        o_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     #获取当前时间
        o_id = self.next_order_id()    #生成订单号
        dao = CartDao()
        data = dao.cart_details(user_id)    #查询当前用户购物车中已经选定的药品和总价
        o_price = data["sum_price"]     #查询当前订单总价
        if self.query("select * from yl_receive where r_user_id=%s",user_id):
            default_id = self.query("select id "\
                                    "from yl_receive where r_default=True ")[0]["id"]
            #插入用户id,订单总价,订单号,订单价格,下单时间到order表中
            self.query(sql1, user_id, o_price, o_id,
                       ORDER_STATUS_NOT_PAY,o_time,default_id)
        else:
            self.query(sql3, user_id, o_price, o_id,
                       ORDER_STATUS_NOT_PAY,o_time)
        data = data['data']
        for i in range(len(data)):
            #将药品id和订单id插入到order_details中
            self.query(sql2,o_id,data[i]["c_med_id"],
             data[i]['c_med_num'],data[i]['price'])





    def order_list(self,user_id):
        #药品图片,名称,总价,单价,订单号,订单状态,创建时间,包装规格,药品数量,药品种类,
        sql1 = """
            select o_med_num,o_med_price,med_img,packing_size,med_name
            from order_detail as o_d inner join medicine as med on o_d.o_goods_id=med.id
            and o_d.o_order_id=%s;
            """
        #总价,状态,创建时间,订单号
        sql2 = "select o_price,o_status,o_id,o_time "\
                "from orders where o_user_id=%s"
        #订单条数
        sql3 = "select count(*)as med_kind from orders where  o_user_id=%s"

        order_ids = []
        data = self.query(sql2,user_id) #订单汇总,订单号,总价,状态,时间
        if not data:
            return "暂无订单"
        for i in data:
            order_ids.append(i["o_id"])
        for i in range(len(order_ids)):
            data1 = self.query(sql1,order_ids[i])
            data[i]["med_detail"] = data1[0]
            data[i]["med_kind"] = self.query(sql3,user_id)[0]["med_kind"]
        return data

    def order_data(self,user_id):
        # 订单创建成功后清空用户购物车中已经选定的药品
        dao = CartDao()
        data = dao.cart_details(user_id)  # 查询当前用户购物车中已经选定的药品和总价
        sum_price = data["sum_price"]
        data = data['data']
        for i in range(len(data)):
            data[i].pop("c_med_id")
            data[i].pop("indications")
        # 清空用户购物车中已经选定的药品
        return {
            'data':data,
            'med_kind':len(data),
            'sum_price':sum_price
        }

    def delete_cart(self,user_id):
        sql = "delete from carts " \
               "where c_user_id=%s and c_is_select=true "
        self.query(sql, user_id)

    def order_details(self,order_id,user_id):
        sql1 = '''               
        select ,r_name,r_phone,r_addr
        from orders as o inner join yl_receive as rec on rec.id=o.o_receive_id
        and o.o_id=%s;
        '''
        sql2 = """
        select o_med_num,o_med_price,med_img,packing_size,med_name
        from order_detail as o_d inner join medicine as med on o_d.o_goods_id=med.id
        and o_d.o_order_id=%s;
        """
        sql3 = "select count(*)as med_kind from order_detail where o_order_id=%s"

        if self.query("select * from yl_receive where r_user_id=%s",user_id):

            data = self.query(sql1,order_id)
        else:
            data = self.query("select o_price,o_status,o_id,o_time "\
                              "from orders where o_id=%s",order_id)
        data1 = self.query(sql2,order_id)   #查询药品详情
        data[0]["med_kind"] = self.query(sql3,order_id)[0]["med_kind"]  #添加药品种类
        data.append(data1)
        return data




