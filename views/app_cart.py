from flask import Blueprint, jsonify, request

from dao.cart_dao import CartDao
from libs.cache import get_token_user_id



blue = Blueprint("cart_api",__name__)
@blue.route('/add_cart/',methods=('GET',))      #添加购物车接口
def add_cart():
    req_data = request.get_json()
    print(req_data,'======')
    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    med_id = req_data['med_id']
    # user_id = 4 # 通过token获取id
    # med_id = 9796

    dao = CartDao()
    data = dao.add_carts(user_id,med_id)       #执行添加购物车函数
    return jsonify({
        "code":200,
        "msg":"添加购物车成功",
        "data":data
    })


@blue.route('/sub_cart/', methods=('GET',))     #删除购物车接口
def sub_cart():
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    med_id = req_data['med_id']
    # user_id = 4  # 通过token获取id
    # med_id = 9793
    dao = CartDao()
    data = dao.sub_carts(user_id,med_id)  # 执行删除购物车函数
    return jsonify({
        "code": 200,
        "msg": "删除购物车成功",
        "data": data
    })

@blue.route('/cart_details/', methods=('GET',))     #购物车详情接口
def cart_detl():
    req_data = request.get_json()
    # print(req_data, '======')
    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    # user_id = 4
    dao = CartDao()
    data = dao.cart_details(user_id)
    return jsonify({
        "code":200,
        "msg":"查询购物车详情成功",
        "data":data
    })

@blue.route('/is_select/', methods=('GET',))     #改变是否选中状态API
def is_select():
    med_id = request.get_json('med_id')
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    # user_id = 4
    # med_id = 9795
    dao = CartDao()
    dao.is_select(user_id,med_id)
    return jsonify({
        "code": 200,
        "msg": "更改选中状态成功",
    })













