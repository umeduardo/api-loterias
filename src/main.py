from flask import Flask, Response, jsonify
from typing import Dict, List, Union, Tuple
from .loader import Loader

app = Flask(__name__)
app.config.update(debug=True)

database = Loader.load_data()

def seleciona_produto(slug_produto):
    produto_selecionado = None
    for produto in Loader.produtos:
        if slug_produto == produto.slug:
            produto_selecionado = produto
    return produto_selecionado

@app.route("/api/estatistica/<produto>", methods=('GET',))
def estatistica(produto) -> Union[Response, Tuple]:

    produto_selecionado = seleciona_produto(produto)
    if produto_selecionado is None:
        return jsonify(['Produto não encontrado']), 404

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
    
    produto_selecionado = seleciona_produto(produto)
    if produto_selecionado is None:
        return jsonify(['Produto não encontrado']), 404

    database_produto: List = database[produto_selecionado.slug]
    result: List = []
    
    if date:
        for resultado in database_produto:
            p = produto_selecionado(resultado)
            if p['data_sorteio'].replace('/', '') == str(date):
                result = [p.get_object()]
    if concurso:
        for resultado in database_produto:
            if p['concurso'] == str(concurso):
                p = produto_selecionado(resultado)
                result = [p.get_object()]
    else:
        for resultado in database_produto:
            p = produto_selecionado(resultado)
            result.append(p.get_object())

    return jsonify(result)


@app.route("/api/sorteios/<produto>", methods=('GET',))
@app.route("/api/sorteios/<produto>/concurso/<concurso>", methods=('GET',))
def resultado(produto, concurso=None) -> Union[Response, Tuple]:

    produto_selecionado = seleciona_produto(produto)
    if produto_selecionado is None:
        return jsonify(['Produto não encontrado']), 404

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