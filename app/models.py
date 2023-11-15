from datetime import date


class Receita:
    def __init__(self, descricao, valor, data, categoria):
        self.id = None  # Vamos definir o ID posteriormente
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": str(self.data),
            "categoria": self.categoria,
        }

    @classmethod
    def from_dict(cls, receita_dict):
        if not isinstance(receita_dict, dict):
            # Se não for um dicionário válido, retorne uma nova instância de Despesa com valores padrão
            return cls()

        # Use get para acessar as chaves do dicionário com segurança
        receita = cls(
            descricao=receita_dict.get("descricao", ""),
            valor=receita_dict.get("valor", 0.0),
            data=receita_dict.get("data", ""),
            categoria=receita_dict.get("categoria", ""),
        )
        receita.id = receita_dict.get("id", None)

        return receita


class Despesa:
    def __init__(self, descricao, valor, data, categoria):
        self.id = None  # Vamos definir o ID posteriormente
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": str(self.data),
            "categoria": self.categoria,
        }

    @classmethod
    def from_dict(cls, despesa_dict):
        if not isinstance(despesa_dict, dict):
            # Se não for um dicionário válido, retorne uma nova instância de Despesa com valores padrão
            return cls()

        # Use get para acessar as chaves do dicionário com segurança
        despesa = cls(
            descricao=despesa_dict.get("descricao", ""),
            valor=despesa_dict.get("valor", 0.0),
            data=despesa_dict.get("data", ""),
            categoria=despesa_dict.get("categoria", ""),
        )

        despesa.id = despesa_dict.get("id", None)

        return despesa
