from flask import Blueprint, render_template,request,redirect,jsonify
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import json

cedula = Blueprint('cedula_routes', __name__ , url_prefix='/cedulas')
con = MongoClient('127.0.0.1') # Conexão com o mongodb
db = con['cedulas'] # chamando a tabela Notas


@cedula.route('/cadastro', methods = ['GET','POST'])
def cadastro_cedula():
# Rota para exibir do dinheiro
    if request.method == 'GET': 
        cedula = list(db.notas.find())
        return render_template('cedulas.html', cedula = cedula)

# Rota para cadastro do dinheiro
    elif request.method == 'POST':
        notas = float(request.values.get('notas'))
        db.notas.insert_one({'notas': notas})
        return redirect('/cedulas/cadastro')

# Rota para atualizar o dinheiro
@cedula.route('/atualiza/<id>', methods=['GET'])
def get_cedula(id):
    pesquisa = db.notas.find({"_id":ObjectId(id)})
    return render_template('atualizar.html', pesquisa=pesquisa)

@cedula.route('/atualiza', methods=['POST'])
def update_notas():
    raw_data = request.values.get('nova')
    id = request.values.get('_id')
    print(raw_data)
    update = db.notas.update({"_id":ObjectId(id)}, {'$set': { "notas" : raw_data }})
    return redirect('/cedulas/cadastro')

#rota para Apagar as notas
@cedula.route('/apagar/<id>')
def apaga_cedula(id):
    obj = ObjectId(id)
    db.notas.delete_one({'_id': obj})
    return redirect('/cedulas/cadastro')
    