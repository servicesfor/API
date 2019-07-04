from flask import Blueprint, jsonify, request

from dao.receive_dao import ReceiveDao
from libs.cache import get_token_user_id


blue = Blueprint("receive_api",__name__)
@blue.route('/add_receive/',methods=('POST',))      #订单列表接口
def add_receive():
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    # user_id = 4
    rec_name = request.form.get("rec_name")
    rec_phone = request.form.get("rec_phone")
    rec_addr = request.form.get("rec_addr")
    dao = ReceiveDao()
    dao.add_receive(user_id,rec_name,rec_phone,rec_addr)
    return jsonify({
        "code":200,
        "msg":"添加收货地址成功!"
    })

@blue.route('/del_receive/',methods=('GET',))      #删除收货地址接口
def del_receive():
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    r_id = req_data["r_id"]
    # r_id = 17
    # user_id = 4
    dao = ReceiveDao()
    dao.del_receive(user_id,r_id)

    return jsonify({
        "code": 200,
        "msg": "删除收货地址成功!"
    })

@blue.route('/change_default/',methods=('GET',))      #更改默认收货地址接口
def change_default():
    req_data = request.get_json()

    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id
    r_id = req_data["r_id"]
    # r_id = 14
    dao = ReceiveDao()
    dao.change_default(r_id)
    return jsonify({
        "code":200,
        "msg":"更改默认收货地址成功"
    })





