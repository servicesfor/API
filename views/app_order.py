from flask import Blueprint, jsonify, request


from dao.order_dao import OrderDao
from libs.cache import get_token_user_id


blue = Blueprint("order_api",__name__)
@blue.route('/order_list/',methods=('GET',))      #订单列表接口
def order_list():
    token = request.args.get("token")

    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(token)  # 通过token获取id

    # user_id = 8 # 通过token获取id
    # med_id = 9796
    dao = OrderDao()
    data = dao.order_list(user_id)

    return jsonify({
        "code": 200,
        "msg": "添加购物车成功",
        "data": data
    })

@blue.route('/order_detail/',methods=('GET',))
def order_detail():
    token = request.args.get("token")

    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(token)  # 通过token获取id
    order_id = request.args.get("order_id")
    # user_id = 5
    # order_id = "2019070400004"
    dao = OrderDao()
    data = dao.order_details(order_id,user_id)  # 执行添加购物车函数
    return jsonify({
        "code": 200,
        "msg": "获取订单详情成功",
        "data": data
    })



@blue.route('/create_order/',methods=('GET',))
def create_order():
    token = request.args.get("token")

    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(token)  # 通过token获取id
    # user_id = 5
    dao = OrderDao()
    dao.create_order(user_id)
    data = dao.order_data(user_id)
    dao.delete_cart(user_id)

    return jsonify({
        "code":200,
        "msg":"下单成功",
        "data":data
    })







