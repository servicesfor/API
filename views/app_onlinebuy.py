from flask import Blueprint
from flask import request, jsonify

from dao.drug_dao import DrugsDao
from logger import api_logger
from datetime import datetime
from libs import cache
from libs.sms import *

blue = Blueprint('app_onlinebuy', __name__)

@blue.route('/medc_illness/',methods=('GET',))
def buy_drug():
    dao = DrugsDao()
    data = dao.find_illness()

    return jsonify({
        "code":200,
        "msg":"查询疾病列表成功",
        "data":data
    })

@blue.route('/drug_details/',methods=('GET',))
def drug_details():
    return jsonify({
        "code": 200,
        "msg": "验证码发送成功",
        "data": "data"
    })
