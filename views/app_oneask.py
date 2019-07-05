from flask import Blueprint, jsonify

from dao.oneask_dao import OneAskDao

blue = Blueprint("oneask_api", __name__)


@blue.route('/one_ask/<int:dep_id>/', methods=('GET',))
def doct_discont(dep_id):
    dao = OneAskDao()
    data = dao.oneask_list(dep_id)
    return jsonify({
        "code": 200,
        "msg": "获取折扣医生详情成功！",
        "data": data
    })
