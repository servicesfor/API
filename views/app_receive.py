from flask import Blueprint, jsonify, request

from dao.receive_dao import ReceiveDao
from libs.cache import get_token_user_id

blue = Blueprint("receive_api", __name__)


@blue.route('/add_receive/', methods=('POST',))  # 添加收货地址接口
def add_receive():
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        rec_name = request.form.get("rec_name")
        rec_phone = request.form.get("rec_phone")
        rec_addr = request.form.get("rec_addr")
        dao = ReceiveDao()
        dao.add_receive(user_id, rec_name, rec_phone, rec_addr)
        return jsonify({
            "code": 200,
            "msg": "添加收货地址成功!"
        })
    except:
        return jsonify({
            "code":400,
            "msg":"添加失败"
        })

@blue.route('/del_receive/', methods=('GET',))  # 删除收货地址接口
def del_receive():
    try:
        token = request.args.get('token')

        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        r_id = request.args.get('rec_id')
        dao = ReceiveDao()
        dao.del_receive(user_id, r_id)

        return jsonify({
            "code": 200,
            "msg": "删除收货地址成功!"
        })
    except:
        return jsonify({
            "code":400,
            "msg":"删除失败"
        })


@blue.route('/change_default/', methods=('GET',))  # 更改默认收货地址接口
def change_default():
    try:
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
    except:
        return jsonify({
            "code":400,
            "msg":"更改默认收货地址失败"
        })


@blue.route('/find_receive/', methods=('GET',))  # 查询收货地址接口
def find_receive():
    try:
        token = request.args.get('token')

        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        r_id = request.args.get('rec_id')
        dao = ReceiveDao()
        data = dao.find_receive(r_id)
        return jsonify({
            "code": 200,
            "msg": "查询收货地址成功",
            "data": data
        })
    except:
        return jsonify({
            "code":400,
            "msg":"查询失败"
        })


@blue.route('/edit_receive/', methods=('POST',))  # 编辑收货地址接口
def edit_receive():
    try:
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
        dao = ReceiveDao()
        dao.edit_receive(rec_name, rec_phone, rec_addr, r_id)
        return jsonify({
            "code": 200,
            "msg": "编辑收货地址成功",
        })
    except:
        return jsonify({
            "code":400,
            "msg":"编辑失败"
        })

@blue.route('/receive_list/', methods=('GET',))  # 展示收货地址列表接口
def receive_list():
    try:
        token = request.args.get('token')

        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })

        user_id = get_token_user_id(token)
        dao = ReceiveDao()
        data = dao.receive_list(user_id)
        return jsonify({
            "code": 200,
            "msg": "查询收货地址列表成功",
            "data": data
        })
    except:
        return jsonify({
            "code":400,
            "msg":"查询失败"
        })







