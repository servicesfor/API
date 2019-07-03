from flask import Blueprint
from flask import request, jsonify
import datetime
from dao.user_dao import UserDao
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
    phone = request.form.get('phone')
    input_code = request.form.get('input_code')
    # 验证上传的必须的数据是否存在
    if not confirm(phone,input_code):   #验证验证码是否一致
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
        })
    req_data = {"phone":phone}    #验证通过之后将验证码从req_data中删除
    dao = UserDao()
    if not dao.check_login_name(phone):     #检测用户名是否存在
        req_data['nick_name'] = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 14))
        req_data['create_time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        req_data['photo'] = 'http://img2.imgtn.bdimg.com/it/u=1813493607,361824557&fm=26&gp=0.jpg'
        req_data['login_auth_str'] = '677698c118bf5e6974f19fd2eb2a5b67'
        req_data['update_time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        req_data['activated'] = "1"
        dao.save(**req_data)                #不存在则存入数据库中,在读取数据

    token = cache.new_token()       #设置新token
    return jsonify({
        'code': 200,
        'msg': 'ok',
        'token':token,
    })

@blue.route('/login_str/', methods=('POST',))
def login_str():
    phone = request.form.get('phone')
    auth_str = request.form.get('auth_str')

    dao = UserDao()
    if dao.check_login_name(phone):         #检测用户名是否存在
        if dao.login_str(phone,auth_str):       #检测密码是否正确
            token = cache.new_token()
            return jsonify({
                'code': 200,
                'msg': 'ok',
                'token':token,
            })
    return jsonify({
        'code': 406,
        'msg': '用户名或密码输入错误',
    })
