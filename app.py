import json
from flask import Flask, jsonify

app = Flask(__name__)

def carregar_dados():
    with open("data/margem.json", "r", encoding="utf-8") as arq_margem, open("data/vidros.json", "r", encoding="utf-8") as arq_vidros, open("data/perfis.json", "r", encoding="utf-8") as arq_perfis, open("data/cores.json", "r", encoding="utf-8") as arq_cores, open ("data/acessorios.json", "r", encoding="utf-8") as arq_acessorios:
        return{
            'margem': json.load(arq_margem),
            'vidros':  json.load(arq_vidros),
            'perfis': json.load(arq_perfis),
            'cores': json.load(arq_cores),
            'acessorios': json.load(arq_acessorios)
        }

@app.route('/')
def index():
    return "Aplicação  de Esquadrias Rodando!"

@app.route('/perfis')
def listar_perfis():
    dados_perfis = carregar_dados()
    return jsonify(dados_perfis['perfis'])

@app.route('/cores')
def listar_cores():
    dados_cores = carregar_dados()
    return jsonify(dados_cores['cores'])

@app.route('/margem')
def listar_margens():
    dados_margem = carregar_dados()
    return jsonify(dados_margem['margem'])

@app.route('/vidros')
def listar_vidros():
    dados_vidros = carregar_dados()
    return jsonify(dados_vidros['vidros'])

@app.route("/acessorios")
def listar_acessorios():
    dados_acessorios = carregar_dados()
    return jsonify(dados_acessorios['acessorios'])

if __name__ == '__main__':
    app.run(debug=True)