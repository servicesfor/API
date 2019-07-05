from flask import Blueprint, jsonify
from dao.diseases_dao import DiseaseDao

blue = Blueprint("diseases_api", __name__)


@blue.route('/look_diseases/', methods=('GET',))
def look_diseases():
    try:
        dao = DiseaseDao()
        data = dao.query_diseases()  # 执行更新昵称函数
        return jsonify({
            'code': 200,
            'msg': '查询疾病成功',
            'data': data
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })


@blue.route('/look_diseases/<int:dis_id>/', methods=('GET',))
def diseases(dis_id):
    try:
        dao = DiseaseDao()
        data = dao.diseases_message(dis_id)  # 执行更新昵称函数
        return jsonify({
            'code': 200,
            'msg': '查询疾病详情成功',
            'data': data
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })
