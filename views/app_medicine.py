from flask import Blueprint
from flask import request, jsonify

from dao.medicine_dao import MedicineDao


blue = Blueprint('app_medicine', __name__)


@blue.route('/medc_illness/', methods=('GET',))
def medc_illness():
    dao = MedicineDao()
    data = dao.find_illness()

    return jsonify({
        "code": 200,
        "msg": "查询疾病列表成功",
        "data": data
    })


@blue.route('/medc_illness/<ill_id>/', methods=('GET',))
def medicine_list(ill_id):
    dao = MedicineDao()
    ill_name = dao.find_illname(ill_id)
    data = dao.medicine_list(ill_name)
    if  data:
        return jsonify({
            "code": 200,
            "msg": "药品列表获取成功",
            "data": data
        })
    return jsonify({
        "code": 400,
        "msg": "药品列表获取失败",
        "data": "暂无该类型药品"
    })


@blue.route('/medc_illness/<med_id>/details/', methods=('GET',))
def medicine_details(med_id):
    dao = MedicineDao()
    data = dao.medicine_details(med_id)
    if data:
        return jsonify({
            "code": 200,
            "msg": "药品详情获取成功",
            "data": data
        })
    return jsonify({
        "code": 400,
        "msg": "药品获取失败",
        "data": "暂无该类型药品"
    })
