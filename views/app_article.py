from flask import Blueprint, jsonify
from dao.article_dao import ArticleDao


blue = Blueprint("article_api",__name__)

@blue.route('/article/',methods=('GET',))
def article_one():
    dao = ArticleDao()
    data = dao.first_page()
    return jsonify({
        'code': 206,
        'msg': '首页查询成功',
        'data':data
    })

@blue.route('/article/<id>/',methods=('GET',))
def article_two(id):
    dao = ArticleDao()
    data = dao.second_page(id)
    return jsonify({
        'code': 206,
        'msg': '文章查询成功',
        'data':data
    })

@blue.route('/science_article/',methods=('GET',))       # 急救大全首页
def science_article():
    dao = ArticleDao()
    data = dao.title_img()
    return jsonify({
        'code': 206,
        'msg': '科普文章查询成功',
        'data':data
    })

@blue.route('/science_articles/<int:id>/',methods=('GET',))     # 文章详情
def science_arti(id):
    dao = ArticleDao()
    data = dao.article_info(id)
    return jsonify({
        'code': 206,
        'msg': '文章详情查询成功',
        'data':data
    })


@blue.route('/recommend_article/<id>/',methods=('GET',))        # 推荐文章
def recom_article(id):
    dao = ArticleDao()
    data = dao.recommend_article(id)
    return jsonify({
        'code': 206,
        'msg': '推荐文章查询成功',
        'data':data
    })