from dao import BaseDao


class CartDao(BaseDao):

    def add_carts(self, c_user_id, c_med_id):  # 添加购物车记录函数
        # 查询该用户购物车中该药品的数量
        sql1 = "select c_med_num,c_med_id from carts " \
               "where c_user_id=%s and c_med_id=%s"
        # 更新用户购物车中药品的数量，在原来的基础上增加1
        sql2 = "update carts set c_med_num=%s where c_user_id=%s and c_med_id=%s"
        # 如果该用户购物车中没有该商品，则在购物车中添加一件该药品
        sql3 = """insert into carts(c_user_id,c_med_id,c_med_num,c_is_select) values (%s,%s,1,True)
        """
        sql4 = """select count(*) as med_kind from carts where c_user_id=%s """
        data = self.query(sql1, c_user_id, c_med_id)  # 查询该用户购物车中该药品的数量
        if data:  # 判断是否有记录
            num = data[0]['c_med_num'] + 1  # 给当前数量加1
            self.query(sql2, num, c_user_id, c_med_id)
            data1 = self.query(sql1, c_user_id, c_med_id)
            data1.append(self.query(sql4, c_user_id)[0])
            return data1  # 返回更新后的药品数量
        self.query(sql3, c_user_id, c_med_id)  # 没有数据添加一条数据
        data2 = self.query(sql1, c_user_id, c_med_id)  # 查询该药品的数量和id
        data2.append(self.query(sql4, c_user_id)[0])  # 查询该用户购物车中的药品种类添加到data2
        return data2  # 返回data2,包含添加药品的id,数量和药品种类

    def sub_carts(self, user_id, med_id):  # 删除购物车记录
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

        data = self.query(sql1, user_id, med_id)  # 查询购物车中数量
        if not data:  # 查询购物车中有没有该药品,没有返回空
            return
        num = data[0]['c_med_num'] - 1  # 更新购物车中数量
        if num > 0:  # 判断药品数量减1后的数量,大于0条更新数据并查找
            self.query(sql2, num, user_id, med_id)  # 更新购物车中的数量，减1
            data = self.query(sql1, user_id, med_id)
            data1 = self.query(sql4, user_id)
            if data1:
                data.append(data1[0])
                return data
            return []
        elif num == 0:  # 更新后药品数量等于0,删除该药
            # 品数据,查询用户购物车中药品种类并返回
            self.query(sql3, user_id, med_id)
            data1 = self.query(sql4, user_id)
            if data1:  # 查询用户购物车是否为空
                return [{
                    'c_med_id': med_id,
                    'c_med_num': 0
                }, data1[0]]
            return [{
                'c_med_id': med_id,
                'c_med_num': 0
            }, {
                "med_kind": 0
            }]

    def cart_details(self, user_id):
        # 联合购物车和药品表,选中查询药品数量,id,图片,单价,包装规格
        sql1 = """
                select c_med_num,c_med_id,med_name,med_img,price,packing_size
                from carts  inner join medicine as med
                on carts.c_med_id=med.id 
                and carts.c_user_id=%s;
                """
        # 通过药品id查询药品适应症
        sql2 = """
                select indications
                from  medicine as med  inner join med_details as det
                on det.med_name_id=med.id 
                and med.id=%s;
                """

        id_l, ind_l = [], []
        SUM_PRICE = 0  # 定义药品详情
        data = self.query(sql1, user_id)  # 查询药品信息

        if not data:  # 判断购物车是否为空
            return '购物车为空'

        for i in range(len(data)):
            id_l.append(data[i]['c_med_id'])  # 将购物车中所有药品id添加到列表id_l中

        for i in range(len(id_l)):  # 循环药品id列表,查询每个药品的适应症
            # 将每个药品的适应症信息添加到ind_l列表中
            ind_l.append(self.query(sql2, id_l[i])[0]['indications'])
            # 将每个药品的适应症加入到药品对象中
            data[i]['indications'] = ind_l[i]
            # 计算每种药品的总价=单价 * 数量
            data[i]['pool_price'] = data[i]['c_med_num'] * data[i]['price']
            # 累加每种药品的总价,计算购物车中所有药品的总价
            SUM_PRICE += data[i]['price']

        # 查询计算购物车中未被选中的所有药品的总价
        NOT_SELECT_PRICE = self.not_select(user_id)
        # 计算购物车中所有选中药品的总价=总价-未被选中药品的总价
        SUM_PRICE -= NOT_SELECT_PRICE
        return {
            "data": data,
            "sum_price": SUM_PRICE
        }

    def not_select(self, user_id):  # 未被选中药品的总价计算
        # 查询药品的数量和单价
        sql = """
                select c_med_num,price
                from carts  inner join medicine as med
                on carts.c_med_id=med.id 
                and carts.c_user_id=%s
                and carts.c_is_select= FALSE
                """

        NOT_SELECT_PRICE = 0
        data = self.query(sql, user_id)  # 查询所有未被选中药品的单价和数量
        if not data:
            return 0
        for i in range(len(data)):
            # 计算未被选中药品的总价 +=单价 * 数量
            NOT_SELECT_PRICE += data[i]["c_med_num"] * data[i]["price"]

        return NOT_SELECT_PRICE

    def is_select(self, user_id, med_id):  # 改变选中状态
        sql = "update carts set c_is_select=not c_is_select where c_user_id=%s and c_med_id=%s"

        self.query(sql, user_id, med_id)

    def del_cart(self, user_id, med_id):
        sql = "delete from carts where c_user_id=%s and c_med_id=%s "
        self.query(sql, user_id, med_id)
