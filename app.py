from flask import Flask,render_template,request,redirect,jsonify
from modulos.cedulasm import cedula
from pymongo import MongoClient, errors
from bson.objectid import ObjectId

app = Flask(__name__)
app.register_blueprint(cedula)
con = MongoClient('127.0.0.1') # Conexão com o mongodb
db = con['cedulas'] # chamando a tabela Notas

# Rota do Index
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/troco', methods=['POST'])
def troco():
    total = float(request.values.get('total'))
    pago = float(request.values.get('pago'))
    notas = list(db.notas.find())
    valor = []
    # converte em lista
    for n in notas:
        valor.append(n['notas'])  
    valor.sort()
    valor.reverse() 
    numNotas = []
    troco = pago - total
    #  quantidade minima de notas
    for i in valor:
        resultado = troco//i
        troco %= i
        dic = {}
        dic[i] = resultado 
        numNotas.append(dic)
    return render_template('home.html', numNotas=numNotas)

if __name__ == '__main__':
    app.run(debug=True)
