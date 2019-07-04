from flask import Blueprint, jsonify, request
from libs.es import ESearch

blue = Blueprint("search_api",__name__)

@blue.route("/home/",methods=('POST',))       # 首页搜索
def search():
    index = request.form.get('index')
    esearch = ESearch('disease_index')
    return jsonify(esearch.query(index))


@blue.route('/doctor_top/',methods=('POST',))     # 问医生搜索
def doctor_top():
    index = request.form.get('index')
    esearch = ESearch('docindex')
    return jsonify(esearch.query(index))

@blue.route('/medcine_search/',methods=('POST',))       #药品搜索
def medicine_search():
    index = request.form.get('index')
    esearch = ESearch('medicine')
    return jsonify(esearch.query(index))
