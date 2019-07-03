from flask import Blueprint, jsonify, request


from dao.order_dao import OrderDao
from libs.cache import get_token_user_id


blue = Blueprint("order_api",__name__)
# @blue.route('/order_list/',methods=('GET',))      #订单列表接口
# def order_list():
#     req_data = request.get_json()
#
#     if not req_data['token']:
#         return jsonify({
#             "code": 400,
#             "msg": "您还未登录,请先登录!"
#         })
#     user_id = get_token_user_id(req_data['token'])  # 通过token获取id
#
#     # user_id = 4 # 通过token获取id
#     # med_id = 9796
#     dao = OrderDao()
#     dao.order_list()
#
#
#
#     return jsonify({
#         "code": 200,
#         "msg": "添加购物车成功",
#         # "data": data
#     })
#
# @blue.route('/order_detail/',methods=('GET',))
# def order_detail():
#     req_data = request.get_json()
#
#     if not req_data['token']:
#         return jsonify({
#             "code": 400,
#             "msg": "您还未登录,请先登录!"
#         })
#     user_id = get_token_user_id(req_data['token'])  # 通过token获取id
#
#
#     dao = OrderDao()
#     data = dao.order_details()  # 执行添加购物车函数

@blue.route('/create_order/',methods=('GET',))
def create_order():
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    # user_id = 4
    dao = OrderDao()
    dao.create_order(user_id)
    data = dao.order_data(user_id)
    dao.delete_cart(user_id)

    return jsonify({
        "code":200,
        "msg":"下单成功",
        "data":data
    })






