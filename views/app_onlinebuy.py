from flask import Blueprint
from flask import request, jsonify

from dao.medicine_dao import MedicineDao
from logger import api_logger
from datetime import datetime
from libs import cache
from libs.sms import *

blue = Blueprint('app_onlinebuy', __name__)

@blue.route('/medc_illness/',methods=('GET',))
def medc_illness():
    dao = MedicineDao()
    data = dao.find_illness()

    return jsonify({
        "code":200,
        "msg":"查询疾病列表成功",
        "data":data
    })

@blue.route('/ill_medicine/<ill_id>/',methods=('GET',))
def medicine_sort(ill_id):


    return jsonify({
        "code": 200,
        "msg": "验证码发送成功",
        "data": "data"
    })
