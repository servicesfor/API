from dao import BaseDao
import random
import base64


class ArticleDao(BaseDao):
    def title_img(self):    # 急救大全首页图片分类
        science_text = {}
        article = []
        recom_article = []
        info = {}
        info1 = {}
        info2 = {}

        sql = 'select subtitle from art_title'
        sql1 ='''
            select article_image.id,article_image.image from art_title inner join article_image on art_title.id=article_image.subtitle_id_id and article_image.subtitle_id_id =1     
        '''
        sql2 ='''
            select article_image.id,article_image.image from art_title inner join article_image
            on art_title.id=article_image.subtitle_id_id and article_image.subtitle_id_id =2     
        '''
        sql3 ='''
            select article_image.id,article_image.image from art_title inner join article_image
            on art_title.id=article_image.subtitle_id_id and article_image.subtitle_id_id =3     
        '''
        sql4 = 'select id,title from articles '
        data = self.query(sql)
        data1 = self.query(sql1)
        data2 = self.query(sql2)
        data3 = self.query(sql3)
        data4 = self.query(sql4)
        info["title"] = data[0]["subtitle"]
        info1["title"] = data[1]["subtitle"]
        info2["title"] = data[2]["subtitle"]
        info["article_info"] = data1
        info1["article_info"] = data2
        info2["article_info"] = data3
        article.append(info)
        article.append(info1)
        article.append(info2)
        for j in range(0,4):
            i = random.randint(0,len(data4))
            recom_article.append(data4[i])
        science_text["article"] = article
        science_text["recom_article"] = recom_article
        return science_text

    def article_info(self,id):  # 查询文章内容
        sql5 = '''
            select articles.title,articles.auth,articles.subjection,articles.content,articles.auth_img,
             articles.title_img from articles inner join article_image on 
             articles.id= article_image.art_cont_id and article_image.id=%s
            ''' % (id)
        data5 = self.query(sql5)
        content = data5[0]["content"]
        content = base64.b64decode(content.encode()).decode()
        data5[0]["content"] = content
        print(content)
        return data5

    def recommend_article(self,id):  # 推荐文章
        sql6 = 'select * from articles where id=%s'%(id)
        data6 = self.query(sql6)
        content = data6[0]["content"]
        content = base64.b64decode(content.encode()).decode()
        data6[0]["content"] = content
        print(content)
        return data6

