import jsonpickle
import os
from models import Despesa, Receita


class SistemaFinanceiro:
    def __init__(self):
        self.receitas = []
        self.despesas = []
        self.categorias_receita = set()
        self.categorias_despesa = set()

    def adicionar_receita(self, receita):
        self.receitas.append(receita)
        self.categorias_receita.add(receita.categoria)

    def adicionar_despesa(self, despesa):
        self.despesas.append(despesa)
        self.categorias_despesa.add(despesa.categoria)

    def carregar_dados(self):
        if os.path.exists("dados.json"):
            with open("dados.json", "r") as arquivo_json:
                dados = jsonpickle.decode(arquivo_json.read())

                receitas_dicts = dados.get("receitas", [])
                despesas_dicts = dados.get("despesas", [])
                categorias_receita = dados.get("categorias_receita", [])
                categorias_despesa = dados.get("categorias_despesa", [])

                # Convertendo os dicionários de receitas para instâncias de Receita
                self.receitas = [
                    Receita.from_dict(receita) for receita in receitas_dicts
                ]

                # Convertendo os dicionários de despesas para instâncias de Despesa
                self.despesas = [
                    Despesa.from_dict(despesa) for despesa in despesas_dicts
                ]

                # Limpar os conjuntos
                self.categorias_receita.clear()
                self.categorias_despesa.clear()

                # Adicionar as categorias ao conjunto
                self.categorias_receita.update(categorias_receita)
                self.categorias_despesa.update(categorias_despesa)

                # Adicionar as categorias globais ao conjunto
                for categoria in dados.get("categorias_receita", []):
                    self.categorias_receita.add(categoria)

                for categoria in dados.get("categorias_despesa", []):
                    self.categorias_despesa.add(categoria)

    def salvar_dados(self):
        dados = {
            "receitas": [receita.to_dict() for receita in self.receitas],
            "despesas": [despesa.to_dict() for despesa in self.despesas],
            "categorias_receita": list(self.categorias_receita),
            "categorias_despesa": list(self.categorias_despesa),
        }
        with open("dados.json", "w") as arquivo_json:
            arquivo_json.write(jsonpickle.encode(dados))

    def __iter__(self):
        return iter(self.receitas + self.despesas)
