from flask import Blueprint, jsonify, request

from dao.order_dao import OrderDao
from libs.cache import get_token_user_id

blue = Blueprint("order_api", __name__)


@blue.route('/order_list/', methods=('GET',))  # 订单列表接口
def order_list():
    try:
        token = request.args.get("token")

        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        dao = OrderDao()
        data = dao.order_list(user_id)

        return jsonify({
            "code": 200,
            "msg": "添加购物车成功",
            "data": data
        })
    except:
        return jsonify({
            "code":400,
            "msg":"获取订单列表成功"
        })


@blue.route('/order_detail/', methods=('GET',))
def order_detail():
    try:
        token = request.args.get("token")
        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        order_id = request.args.get("order_id")
        dao = OrderDao()
        data = dao.order_details(order_id, user_id)  # 执行添加购物车函数
        return jsonify({
            "code": 200,
            "msg": "获取订单详情成功",
            "data": data
        })
    except:
        return jsonify({
            "code":400,
            "msg":"获取订单详情失败"
        })


@blue.route('/create_order/', methods=('GET',))     #创建订单
def create_order():
    try:
        token = request.args.get("token")

        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        dao = OrderDao()
        dao.create_order(user_id)
        data = dao.order_data(user_id)
        dao.delete_cart(user_id)

        return jsonify({
            "code": 200,
            "msg": "下单成功",
            "data": data
        })
    except:
        return jsonify({
            "code": 200,
            "msg": "下单失败"
        })

@blue.route('/pay_order/', methods=('POST',))     #支付订单
def pay_order():
    try:
        token = request.args.get("token")
        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        order_id = request.form.get("order_id")
        user_id = get_token_user_id(token)
        pay_pwd = request.form.get("pay_str")   # 支付密码
        dao = OrderDao()
        msg = dao.pay_order(user_id,order_id,pay_pwd)
        return jsonify({
            "code":200,
            "msg":msg
        })
    except:
        return jsonify({
            "code":400,
            "msg":"支付失败"
        })

