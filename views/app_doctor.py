from flask import Blueprint, jsonify

blue1 = Blueprint("doctor_api",__name__)


@blue1.route('/find_doctor/',methods=('GET',))
def find_doctor():
    sql = "select * from departments"


    return jsonify({
        'code': 201,
        'msg': '问医生'
    })


@blue1.route('/hospital/',methods=("GET"))
def hospital():





@blue1.route('/article/',methods=('GET',))
def article():





@blue1.route('/diseases/',methods=('GET',))
def find_diseases():


