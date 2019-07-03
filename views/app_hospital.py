from flask import Blueprint, jsonify

from dao.hospital_dao import HospitalDao

blue = Blueprint("hospital_api", __name__)


@blue.route('/hospital_detail/<hospid>/', methods=("GET",))     #医院详情API
def hospital(hospid):
    dao = HospitalDao()
    hosp = dao.hosp_detail(hospid)
    return jsonify({
        "code":200,
        "msg":"获取医院信息成功！",
        "hosp":hosp
    })


