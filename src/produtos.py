from abc import ABC, abstractmethod
from typing import Dict, List

class Product(ABC):

    bolas: list
    slug: str
    campo: str
    dados: Dict
    quantidade_numeros: int

    def __init__(self, dados):
        self.dados = dados
    
    def get_resultado(self):
        resultado: List = []
        for num in range(self.bolas[0], self.bolas[1]+1):
            column_name = '{}{}'.format(self.campo, num)
            resultado.append(int(self.dados[column_name]))
        return resultado


    @abstractmethod
    def get_premio(self):
        pass

    def get_object(self):
        return {
            "concurso": self.dados['concurso'],
            "data_sorteio": self.dados['data_do_sorteio'],
            "premio": self.get_premio(),
            "resultado": self.get_resultado(),
        }

class Lotofacil(Product):
    
    bolas: list = [1,15]
    slug: str = 'lotofacil'
    campo: str = 'bola'
    premios: List = [11,12,13,14,15]
    quantidade_numeros = 25

    def get_premio(self):
        result: List = []
        
        for premio in self.premios:{
            result.append({
                'pontos': f'{premio} pontos',
                'ganhadores': self.dados[f'ganhadores_{premio}_numeros'],
                'premio': self.dados[f'ganhadores_{premio}_numeros']})
        }
        return result


class Megasena(Product):
    bolas: list = [1,6]
    slug: str = 'megasena'
    campo: str = 'coluna_'
    premios: List = ['faixa_1','faixa_2','faixa_3']
    quantidade_numeros = 60

    quantidade_pontos: Dict = {'faixa_1': 6, 'faixa_2': 5, 'faixa_3': 4}

    def get_premio(self):
        result: List = []
        for premio in self.premios:{
            result.append({
                'pontos': self.quantidade_pontos[premio],
                'ganhadores': self.dados[f'ganhadores_{premio}'],
                'premio': self.dados[f'ganhadores_{premio}']})
        }
        return result
