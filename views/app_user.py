import os
import uuid

from flask import Blueprint
from flask import request, jsonify
import datetime

from werkzeug.datastructures import FileStorage

from dao import BaseDao
from dao.user_dao import UserDao
from libs import cache, oss
from libs.cache import get_token_user_id, save_token
from libs.crypt import make_password
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
    user_id = dao.find_userid(phone)
    print(user_id,"前面的")
    token = cache.new_token()       #设置新token
    save_token(token,user_id)
    user_id = get_token_user_id(token)
    print(user_id,'********************')
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
            user_id = dao.find_userid(phone)
            save_token(token, user_id)
            return jsonify({
                'code': 200,
                'msg': 'ok',
                'token':token,
            })
    return jsonify({
        'code': 406,
        'msg': '用户名或密码输入错误',
    })

@blue.route('/mine/', methods=('GET',))
def mine():
    req_data = request.get_json()
    if not req_data['token']:
        return jsonify({
            "code": 400,
            "msg": "您还未登录,请先登录!"
        })
    user_id = get_token_user_id(req_data['token'])  # 通过token获取id

@blue.route('/own_page/',methods=('POST',))   #通过token查询个人信息
def own_first_page():
    token = request.form.get("token")   #需要上传token
    try:
        u_id = get_token_user_id(token)
        dao = UserDao()
        data = dao.return_own_mes(u_id)
        return jsonify({
            'code':200,
            "msg":'个人页面查询成功',
            "data":data
        })
    except:
        return jsonify({
            'code':405,
            'msg':'请先注册或登录'
        })



@blue.route('/focus_doctor/',methods=('GET',))  #关注医生和取消关注功能接口
def foc_doc():
    token = request.args.get("token")      #用户token
    doc_id = request.args.get("doctor_id")  #关注医生的id
    try:
        u_id = get_token_user_id(token)
        dao = UserDao()
        dao.focus_doctors(doc_id,u_id)
        return jsonify({
            'code':200,
            "msg":'关注医生成功',
        })
    except:
        return jsonify({
            'code':405,
            'msg':'请先注册或登录'
        })

@blue.route('/collect_art/',methods=('GET',))  #收藏和取消收藏文章接口
def collect_art():
    token = request.args.get("token")      #用户token
    art_id = request.args.get("art_id")  #收藏和取消的文章id
    try:
        u_id = get_token_user_id(token)
        dao = UserDao()
        dao.collect_art(art_id,u_id)
        return jsonify({
            'code':200,
            "msg":'收藏文章成功',
        })
    except:
        return jsonify({
            'code':405,
            'msg':'请先注册或登录'
        })

@blue.route('/my_collect/', methods=('GET',))  # 通过token查询我的收藏
def collect_article():
    token = request.args.get("token")
    try:
        u_id = get_token_user_id(token)
        dao = UserDao()
        data = dao.collect_article(u_id)
        return jsonify({
            'code':200,
            "msg":'我的收藏查询成功',
            "data":data
        })
    except:
        return jsonify({
            'code':405,
            'msg':'请先注册或登录'
        })

@blue.route('/my_focus/', methods=('GET',))  # 我的关注医生
def my_focus():
    token = request.args.get("token")
    try:
        u_id = get_token_user_id(token)
        dao = UserDao()
        data = dao.my_focus(u_id)
        return jsonify({
            'code':200,
            "msg":'我的关注查询成功',
            "data":data
        })
    except:
        return jsonify({
            'code':405,
            'msg':'请先注册或登录'
        })


@blue.route('/update_phone/',methods=('POST',)) # 更改手机号发送验证码
def update_ph():
    dao = UserDao()
    phone = request.form.get('phone')
    data = dao.update_phone(phone)
    return jsonify({
        "code":200,
        "data":data
    })


@blue.route('/change_phone/', methods=('POST',))     # 验证验证码
def check_code():
    dao = UserDao()
    token = request.args.get('token')  # 获取form中的token
    user_id = get_token_user_id(token)  # 通过token获取id
    # 前端请求的Content-Type: application/json
    phone = request.form.get('phone')
    input_code = request.form.get('input_code')
    # 验证上传的必须的数据是否存在
    if not confirm(phone,input_code):   #验证验证码是否一致
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
        })
    dao.update_Verifi(phone,user_id)
    return jsonify({
        "code":200,
        "msg":"更改手机号成功"
    })

@blue.route('/forget_pwd/', methods=('POST',))     # 忘记密码接口
def forget_pwd():
    phone = request.form.get('phone')
    dao = UserDao()
    data = dao.forget_pwd(phone)
    return jsonify({
        "code": 200,
        "data": data
    })

@blue.route('/check_code/', methods=('POST',))     # 验证验证码接口
def checking_code():
    phone = request.form.get('phone')
    input_code = request.form.get('input_code')
    # 验证上传的必须的数据是否存在
    if not confirm(phone,input_code):   #验证验证码是否一致
        return jsonify({
            "code":400,
            "msg":"验证码输入错误,请重新输入",
        })
    token = cache.new_token()  # 设置新token
    dao = UserDao()
    user_id = dao.find_userid(phone)
    save_token(token, user_id)
    return jsonify({
        'code': 200,
        'msg': 'ok',
        'token': token,
    })

@blue.route('/new_password/', methods=('POST',))
def new_password():
    token = request.form.get('token')
    auth_str = npwd = request.form.get("auth_str")
    make_password(npwd)
    user_id = get_token_user_id(token)
    dao = UserDao()
    dao.new_password(auth_str,user_id)
    return jsonify({
        'code': 200,
        'msg': '更改密码成功'
    })



@blue.route('/upload_avator/', methods=('POST',))   #更换头像
def upload_avator():
    # 上传的头像字段为 img
    # 表单参数： token
    file: FileStorage = request.files.get('img', None)
    token = request.args.get('token', None)

    if all((bool(file), bool(token))):
        # 验证文件的类型, png/jpeg/jpg, 单张不能超过2M
        # content-type: image/png, image/jpeg
        print(file.content_length, 'bytes')
        if file.content_type in ('image/png',
                                 'image/jpeg'):
            filename = uuid.uuid4().hex \
                       + os.path.splitext(file.filename)[-1]
            file.save(filename)

            # 上传到oss云服务器上
            key = oss.upload_file(filename)

            os.remove(filename)  # 删除临时文件

            token = request.args.get('token')
            # 将key写入到DB中
            id = get_token_user_id(token)

            sql = "update yl_user set photo=(%s) where id=%s"
            db = BaseDao()
            db.query(sql,key,id)

            return jsonify({
                'code': 200,
                'msg': '上传文件成功',
                'file_key': key
            })
        else:
            return jsonify({
                'code': 201,
                'msg': '图片格式只支持png或jpeg'
            })

    return jsonify({
        'code': 100,
        'msg': 'POST请求参数必须有img和token'
    })


@blue.route('/img_url/', methods=('GET', ))     #获取头像
def get_img_url():
    token = request.args.get('token')
    id = get_token_user_id(token)
    sql = "select photo from yl_user where id=%s"
    db=BaseDao()
    dic_key = db.query(sql,id)[0]
    key = dic_key['photo']
    img_url = oss.get_small_url(key)
    return jsonify({
        'url': img_url
        })






