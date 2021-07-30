from flask import Flask, Response, jsonify
from typing import Dict, List, Union, Tuple
from .loader import Loader
from .produtos import Product

app = Flask(__name__)
app.config.update(debug=True)

database = Loader.load_data()

@app.route('/')
def index():
    return jsonify({
        'doc': 'Documentacao dp Loterias API',
        'produtos': ['megsaena', 'lotofacil'],
        'endpoints': [
            {
                '/': 'This document.',
                '/api/resultados/<produto>': 'Todos os resultados de um produto',
                '/api/resultados/<produto>/data/<data>': 'Resultados de um produto por data. Formato: ddmmaaa',
                '/api/resultados/<produto>/concurso/<concurso>': 'Resultados de um produto por concurso.',
                '/api/estatistica/<produto>': 'Estatística de saída de cada número por produto.',
            }
        ]
    })

@app.route("/api/estatistica/<produto>", methods=('GET',))
def estatistica(produto) -> Union[Response, Tuple]:

    try:
        produto_selecionado = Product.create(produto, Loader.produtos)
    except Exception as e:
        return jsonify(str(e)), 404

    resultados_produto: List = database[produto]

    quantidade_concursos: int = len(resultados_produto)
    quantidade_sorteios: Dict = {}

    for resultado in resultados_produto:
        p = produto_selecionado(resultado)
        dados: Dict = p.get_resultado()
        
        for num in dados:
            quantidade_sorteios[num] = quantidade_sorteios.get(num, 0) + 1


    result: Dict = {}
    for num in range(1,produto_selecionado.quantidade_numeros+1):
        result[num] = round(quantidade_sorteios.get(num, 0) / quantidade_concursos,2)
        
    return jsonify(result)


@app.route('/api/resultados/<produto>', methods=['GET'])
@app.route('/api/resultados/<produto>/data/<date>', methods=['GET'])
@app.route('/api/resultados/<produto>/concurso/<concurso>', methods=['GET'])
def sorteios(produto, date=None, concurso=None) -> Union[Response, Tuple]:
    
    try:
        produto_selecionado = Product.create(produto, Loader.produtos)
    except Exception as e:
        return jsonify(str(e)), 404

    database_produto: List = database[produto_selecionado.slug]
    result: List = []
    if date:
        for resultado in database_produto:
            p = produto_selecionado(resultado)
            obj = p.get_object()
            print(obj['data_sorteio'].replace('/', ''))
            if obj['data_sorteio'].replace('/', '') == str(date):
                result = [obj]
    elif concurso:
        for resultado in database_produto:
            p = produto_selecionado(resultado)
            obj = p.get_object()
            if obj['concurso'] == str(concurso):
                result = [obj]
    else:
        for resultado in database_produto:
            p = produto_selecionado(resultado)
            result.append(p.get_object())

    return jsonify(result)


@app.route("/api/sorteios/<produto>", methods=('GET',))
@app.route("/api/sorteios/<produto>/concurso/<concurso>", methods=('GET',))
def resultado(produto, concurso=None) -> Union[Response, Tuple]:

    try:
        produto_selecionado = Product.create(produto, Loader.produtos)
    except Exception as e:
        return jsonify(str(e)), 404

    result: List = []
    resultados_produto: Dict = database[produto]

    for resultado in resultados_produto:
        p = produto_selecionado(resultado)
        dados: Dict = p.get_resultado()
        
        if resultado['concurso'] == concurso:
            result = [dados]
            break

        result.append(dados)
        
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
