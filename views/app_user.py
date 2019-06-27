from flask import Blueprint
from flask import request, jsonify

from libs.cache import new_token, save_token
from logger import api_logger
from dao.user_dao import UserDao
from datetime import datetime
from libs import cache
from libs.sms import *

blue = Blueprint('user_api', __name__)

@blue.route('/send_code/',methods=('POST',))
def send_code():
    phone = request.form.get('phone')
    new_code(phone)
    return jsonify({
        "code":200,
        "msg":"验证码发送成功"
    })



@blue.route('/regist/', methods=('POST',))
def user_regist():
    # 前端请求的Content-Type: application/json
    req_data = None
    api_logger.info(request.headers)
    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()
        print("req_data",req_data)

    if req_data is None:
        api_logger.warn('%s 请求参数未上传-json' % request.remote_addr)
        return jsonify({
            'code': 9000,
            'msg': '请上传json数据，且参数必须按api接口标准给定'
        })

    api_logger.debug(req_data)

    phone = req_data['phone']
    input_code = req_data['input_code']
    # 验证上传的必须的数据是否存在
    if not confirm(phone,input_code):
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
            'data':req_data
        })
    dao = UserDao()
    dao.save(**req_data)

    token = cache.new_token()
    return jsonify({
        'code': 200,
        'msg': 'ok',
        'data': req_data
    })


@blue.route('/login/', methods=('POST',))
def user_login():
    api_logger.debug('user login get action!')
    # 验证参数
    login_name = request.form.get('login_name', None)
    auth_str = request.form.get('auth_str', None)
    if all((bool(login_name), bool(auth_str))):
        dao = UserDao()
        # 获取登录用户的信息
        try:
            login_user = dao.login(login_name, auth_str)
            # 生成token
            token = cache.new_token()

            # 将token存在redis的缓存中，绑定的数据可以是用户Id也可以是用户的信息
            cache.save_token(token, login_user.get('user_id'))
            return jsonify({
                'code': 200,
                'token': token,
                'user_data': login_user
            })
        except Exception as e:
            return jsonify({
                'code': 202,
                'msg': e
            })
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数login_name和auth_str必须存在'
        })
