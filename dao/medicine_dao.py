import random

from flask import url_for

from dao import BaseDao
from logger import api_logger

details = [['痘痘', '黑头', '脱发', '避孕', '阳痿', '感冒', '脚气', '痔疮'],
           ['支气管炎', '鼻炎', '慢阻肺', '肺结核', '肺炎', '哮喘', '其他'],
           ['皮炎/癣症', '脱发/头屑', '痔疮', '黄褐斑', '蚊虫叮咬', '灰指甲', '银屑病', '白癜风', '疱疹', '其他'],
           ['腹痛腹泻', '消化不良', '便秘', '胃炎', '胃肠溃疡', '结肠炎', '小儿肠胃病', '寄生虫', '胃酸过多', '其他']]


class MedicineDao(BaseDao):

    def find_illness(self):  # 列表详情
        # 查询疾病id和name
        global details
        classify = ['常见症状', '呼吸系统', '皮肤问题', '消化系统']

        list1, list2 = [], []
        for i in range(len(classify)):  # 遍历疾病分类
            for j in range(len(details[i])):  # 遍历小分类
                if i == 0:  # 常见疾病分类需要添加图片
                    data = {
                        'id': str(i) + str(j),
                        'name': details[i][j],
                        'img': url_for('static', filename="ill_img/" + str(details[i][j]) + ".jpg")
                    }
                else:
                    data = {
                        'id': str(i) + "-" + str(j),
                        'name': details[i][j],
                    }
                list1.append(data)  # 将所有的小分类对象添加到list1中
            list2.append(list1)  # 将所有的疾病对象添加到李斯特中
            list1 = []
        return list2

    def find_illname(self, ill_id):

        list1 = ill_id.split('-')  # 分割疾病id为大小分类
        return details[int(list1[0])][int(list1[1])]  # 提取疾病id对应的疾病名称

    def medicine_list(self, ill_name):  # 药品列表显示

        # 通过疾病类型对应药品适应症模糊查询相关药品信息
        sql1 = "select med_name_id as med_id from med_details WHERE indications LIKE %s"
        # 查询药品id,名称,图片,价格,包装规格,国药准字,库存
        sql2 = """SELECT id,med_name,med_img,price,packing_size,approval_number,med_stock 
              FROM medicine where id=%s
               """
        list2,data = [],[]

        ill_name = '%' + ill_name + '%'     #配置查询条件
        list1 = self.query(sql1, ill_name)  # 查询药品id信息
        if not list1:  # 判断药品信息是否为空
            return
        for i in range(len(list1)):
            list2.append(list1[i]['med_id'])  # 将药品id提取到list1列表
        for j in list2:
            data.append(self.query(sql2, j)[0])  # 通过药品id查找药品信息,添加到list2列表中
        return data

    def medicine_details(self, med_id):  # 通过药品id查询药品详情
        sql = """
        select med.id as med_id, med_name as '药品名', med_img, price, med_stock as '库存', approval_number as '国药准字', packing_size as '包装规格', med_formulation as '剂型', composition as '药品成分', shape as '性状', indications as '适应症', pdc_date as '生产日期', validity_period as '有效期', manufacturer as '制造商', med_interact as '药品相互作用', attentions as '注意事项', taboo as '禁忌', reaction as '不良反应', pharm_toxicity as '药理毒理', det.storage as '贮藏'
        from medicine as med inner join med_details as det
        on med.id=det.med_name_id
        and med.id=%s
        """

        return self.query(sql, med_id)
