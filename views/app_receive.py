from flask import Blueprint, jsonify, request

from dao.receive_dao import ReceiveDao
from libs.cache import get_token_user_id

blue = Blueprint("receive_api", __name__)


@blue.route('/add_receive/', methods=('POST',))  # 添加收货地址接口
def add_receive():
    token = request.args.get('token')
    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(token)  # 通过token获取id
    # user_id = 4
    rec_name = request.form.get("rec_name")
    rec_phone = request.form.get("rec_phone")
    rec_addr = request.form.get("rec_addr")
    dao = ReceiveDao()
    dao.add_receive(user_id, rec_name, rec_phone, rec_addr)
    return jsonify({
        "code": 200,
        "msg": "添加收货地址成功!"
    })


@blue.route('/del_receive/', methods=('GET',))  # 删除收货地址接口
def del_receive():
    token = request.args.get('token')

    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(token)  # 通过token获取id
    r_id = request.args.get('rec_id')
    # r_id = 17
    # user_id = 4
    dao = ReceiveDao()
    dao.del_receive(user_id, r_id)

    return jsonify({
        "code": 200,
        "msg": "删除收货地址成功!"
    })


@blue.route('/change_default/', methods=('GET',))  # 更改默认收货地址接口
def change_default():
    token = request.args.get('token')
    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    # r_id = 14
    user_id = get_token_user_id(token)
    r_id = request.args.get('rec_id')
    dao = ReceiveDao()
    dao.change_default(r_id, user_id)
    return jsonify({
        "code": 200,
        "msg": "更改默认收货地址成功"
    })


@blue.route('/find_receive/', methods=('GET',))  # 查询收货地址接口
def find_receive():
    token = request.args.get('token')

    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })

    # r_id = 14
    r_id = request.args.get('rec_id')
    dao = ReceiveDao()
    data = dao.find_receive(r_id)
    return jsonify({
        "code": 200,
        "msg": "查询收货地址成功",
        "data": data
    })


@blue.route('/edit_receive/', methods=('POST',))  # 编辑收货地址接口
def edit_receive():
    token = request.args.get('token')  # 获取token
    if not token:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    rec_name = request.form.get("rec_name")
    rec_phone = request.form.get("rec_phone")
    rec_addr = request.form.get("rec_addr")
    r_id = request.args.get("rec_id")
    # r_id = 14
    dao = ReceiveDao()
    dao.edit_receive(rec_name, rec_phone, rec_addr, r_id)
    return jsonify({
        "code": 200,
        "msg": "编辑收货地址成功",
    })
