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

@blue.route('/login_code/', methods=('POST',))
def login_code():
    # 前端请求的Content-Type: application/json
    req_data = None
    api_logger.info(request.headers)
    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()

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
        # req_data.pop('input_code')
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
        })
    req_data.pop('input_code')
    dao = UserDao()
    if dao.check_login_name(phone):
        result = dao.login_data(phone)
    else:
        dao.save(**req_data)
        result = dao.login_data(phone)
    token = cache.new_token()
    return jsonify({
        'code': 200,
        'msg': 'ok',
        'token':token,
        'data': result
    })

@blue.route('/login_str/', methods=('POST',))
def login_str():
    # 前端请求的Content-Type: application/json
    req_data = None
    api_logger.info(request.headers)
    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()

    if req_data is None:
        api_logger.warn('%s 请求参数未上传-json' % request.remote_addr)
        return jsonify({
            'code': 9000,
            'msg': '请上传json数据，且参数必须按api接口标准给定'
        })

    api_logger.debug(req_data)

    phone = req_data['phone']
    auth_str = req_data.get('auth_str')
    # 验证上传的必须的数据是否存在

    dao = UserDao()
    if dao.check_login_name(phone):
        if dao.login_str(phone,auth_str):
            login_data = dao.login_data(phone)
            token = cache.new_token()
            result = {
                'code': 200,
                'msg': 'ok',
                'token':token,
                'data': login_data
            }
            return jsonify(result)
    return jsonify({
        'code': 406,
        'msg': '用户名或密码输入错误',
    })
