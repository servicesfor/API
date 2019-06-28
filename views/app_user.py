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
    if not confirm(phone,input_code):   #验证验证码是否一致
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
        })
    req_data.pop('input_code')      #验证通过之后将验证码从req_data中删除
    dao = UserDao()
    if dao.check_login_name(phone):     #检测用户名是否存在

        result = dao.login_data(phone)      #已存在则直接读取数据库数据
        result[0].pop('login_auth_str')
        result[0]["my_focus"] = dao.focus_doctors(result['id'])
    else:
        dao.save(**req_data)                #不存在则存入数据库中,在读取数据
        result = dao.login_data(phone)
    token = cache.new_token()       #设置新token
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
    if dao.check_login_name(phone):         #检测用户名是否存在
        if dao.login_str(phone,auth_str):       #检测密码是否正确
            login_data = dao.login_data(phone)
            login_data[0].pop('login_auth_str')
            token = cache.new_token()
            return jsonify({
                'code': 200,
                'msg': 'ok',
                'token':token,
                'data': login_data
            })
    return jsonify({
        'code': 406,
        'msg': '用户名或密码输入错误',
    })
