from flask import Blueprint
from flask import request, jsonify
from logger import api_logger
from dao.user_dao import UserDao
from datetime import datetime
from libs import cache
from libs.sms import *

blue = Blueprint('user_api', __name__)

@blue.route('/buy_drug/',methods=('GET',))
def buy_drug():

    return jsonify({
        "code":200,
        "msg":"验证码发送成功",
        "data":"data"
    })
@blue.route('/drug_details/',methods=('GET',))
def drug_details():
    return jsonify({
        "code": 200,
        "msg": "验证码发送成功",
        "data": "data"
    })
