import operator

from flask import Blueprint, jsonify, request

from dao import BaseDao
from dao.doctor_dao import DoctorDao
from dao.user_dao import UserDao
from libs.cache import get_token_user_id

blue = Blueprint("doctor_api", __name__)


@blue.route('/ask_doctor/', methods=('GET',))
def ask_doctor():
    # 科室id列表
    ofc_list = [[i for i in range(1, 10)],
                [6, 24, 25, 26, 27, 28],
                [4, 15, 16, 17, 19, 20],
                [10, 11, 12, 13, 14, 18, 21, 22, 23]]

    dao = DoctorDao()
    ofc_data = dao.find_ofc(ofc_list)  # 查询科室信息

    return jsonify({
        'code': 201,
        'msg': '问医生',
        'ofc_data': ofc_data
    })


@blue.route('/ask_doctor/<int:depid>/', methods=('GET',))  # 医生列表
def doct_list(depid):
    try:
        dao = DoctorDao()
        doct_data = dao.find_doct(depid)

        return jsonify({
            "code": 200,
            "msg": "获取医生列表成功",
            "doct_data": doct_data
        })
    except:
        return jsonify({
            "code": 400,
            "msg": "获取医生列表失败",
        })


@blue.route('/ask_doctor/<docid>/detail/', methods=("GET",))
def doctor_resume(docid):  # 医生履历
    try:
        dao = DoctorDao()
        doc_detail = dao.doct_resume(docid)  # 医生履历查询
        return jsonify({
            "code": 200,
            "msg": "获取医生履历成功",
            "doc_detail": doc_detail
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })


@blue.route('/ask_doctor/<doc_id>/resume/', methods=('GET',))
def doct_detail(doc_id):  # 医生详情
    try:
        dao = DoctorDao()
        doct_data = dao.doctor_detail(doc_id)
        return jsonify({
            "code": 200,
            "msg": "获取医生详情成功！",
            "data": doct_data
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })


@blue.route('/patient_list/', methods=('GET',))  # 获取患者列表API
def pat_list():  # 获取患者列表
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({
                "code": 400,
                "msg": "您还未登录,请先登录!"
            })
        user_id = get_token_user_id(token)  # 通过token获取id
        dao = UserDao()
        pat = dao.patient_list(user_id)
        return jsonify({
            "code": 200,
            "msg": "获取患者列表成功！",
            "data": pat
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })


@blue.route('/patient/', methods=('POST', 'PATCH',))  # 添加患者信息API
def patient_message():
    try:
        req_data = {}
        token = request.args.get('token')  # 获取form中的token
        req_data['p_user_id'] = get_token_user_id(token)  # 通过token获取id
        req_data['p_name'] = request.form.get('p_name')  # 患者姓名
        req_data['p_ID_number'] = request.form.get('p_ID_number')  # 身份证号
        req_data['p_sex'] = request.form.get('p_sex')  # 性别
        req_data['date_birth'] = request.form.get('date_birth')  # 出生日期
        req_data['p_weight'] = request.form.get('p_weight')  # 体重
        req_data['is_allergy'] = request.form.get('is_allergy')  # 过敏史
        req_data['medical_history'] = request.form.get('medical_history')  # 过往病史
        req_data['is_normal_liver'] = request.form.get('is_normal_liver')  # 肝功
        req_data['is_normal_kidney'] = request.form.get('is_normal_kidney')  # 肾功
        req_data['is_pregnancy_preparation'] = request.form.get('is_pregnancy_preparation')  # 是否备孕
        patient_dao = BaseDao()
        patient_dao.save('patient', **req_data)
        return jsonify({
            'code': 200,
            'msg': '添加患者信息成功'
        })
    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })


@blue.route('/socket_doc/', methods=('GET',))  # 医生排序
def socket_doc():
    try:
        value = int(request.args.get("value"))
        dep_id = request.args.get("depid")
        dao = DoctorDao()
        data = dao.find_doct(dep_id)  # 按科室查询医生数据
        # 将查询到的数据进行排序
        if value == 0:  # 综合排序
            pass
        elif value == 1:  # 星级排名
            data = sorted(data, key=operator.itemgetter('d_level'))
        elif value == 2:  # 回复时间排名
            data = sorted(data, key=operator.itemgetter('avg_response'))
        elif value == 3:  # 价格升序排名
            data = sorted(data, key=operator.itemgetter('text_price'))
        elif value == 4:  # 价格降序排名
            data = sorted(data, key=operator.itemgetter('text_price'), reverse=True)
        elif value == 5:  # 回答次数降序排名
            data = sorted(data, key=operator.itemgetter('m_answer'), reverse=True)
        return jsonify({
            "code": 200,
            "msg": "获取医生列表成功",
            "data": data
        })

    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })

@blue.route('/area_find/')      #按地区查找医生
def area_find():
    try:
        area = request.args.get("area")
        dao = DoctorDao()
        data = dao.area_find(area)
        return jsonify({
            "code":200,
            "msg":"获取医生信息成功",
            "data":data
        })

    except:
        return jsonify({
            'code': 400,
            'msg': '暂无数据'
        })













