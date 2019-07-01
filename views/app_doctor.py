from flask import Blueprint, jsonify

from dao.doctor_dao import DoctorDao

blue1 = Blueprint("doctor_api",__name__)

@blue1.route('/ask_doctor/',methods=('GET',))
def ask_doctor():
    #科室id列表
    ofc_list = [[i for i in range(1, 10)],
                [6, 24, 25, 26, 27],
                [4, 15, 16, 17, 19, 20] ,
                [10, 11, 12, 13, 14, 18, 21, 22, 23]]

    dao = DoctorDao()
    ofc_data = dao.find_ofc(ofc_list)       #查询科室信息

    return jsonify({
        'code': 201,
        'msg': '问医生',
        'ofc_data':ofc_data
    })

@blue1.route('/ask_doctor/<int:depid>/<int:page_num>/',methods=('GET',))
def doct_list(depid,page_num):
    values = {"depid":depid,"page_num":page_num}
    dao = DoctorDao()
    doct_data = dao.find_doct(**values)

    return jsonify({
        "code":200,
        "msg":"获取医生列表成功",
        "doct_data":doct_data
    })

@blue1.route('/ask_doctor/<docid>/detail/',methods=("GET",))
def doctor_resume(docid):     #医生履历
    dao = DoctorDao()
    doc_detail = dao.doct_resume(docid)     #医生履历查询
    return jsonify({
        "code":200,
        "msg":"获取医生履历成功",
        "doc_detail":doc_detail
    })

@blue1.route('/ask_doctor/<doc_id>/resume/',methods=('GET',))
def doct_detail(doc_id):        #医生详情
    dao = DoctorDao()
    doct_data = dao.doctor_detail(doc_id)
    return jsonify({
        "code":200,
        "msg":"获取医生详情成功！",
        "data":doct_data
    })

# @blue1.route('/hospital/',methods=("GET"))
# def hospital():
#
#
#
#
#
# @blue1.route('/article/',methods=('GET',))
# def article():
#
#
#
#
#
# @blue1.route('/diseases/',methods=('GET',))
# def find_diseases():


