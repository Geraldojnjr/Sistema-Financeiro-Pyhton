from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from calendar import monthrange
import json
import jsonpickle
import os

app = Flask(__name__)

# Classe Receita
class Receita:
    def __init__(self, descricao, valor, data, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def to_dict(self):
        return {
            'descricao': self.descricao,
            'valor': self.valor,
            'data': str(self.data),
            'categoria': self.categoria
        }

# Classe Despesa
class Despesa:
    def __init__(self, descricao, valor, data, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def to_dict(self):
        return {
            'descricao': self.descricao,
            'valor': self.valor,
            'data': str(self.data),
            'categoria': self.categoria
        }

# Classe SistemaFinanceiro
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

    # Método carregar_dados na classe SistemaFinanceiro
    def carregar_dados(self):
        if os.path.exists('dados.json'):
            with open('dados.json', 'r') as arquivo_json:
                dados = jsonpickle.decode(arquivo_json.read())
                
                receitas_dicts = dados.get('receitas', [])
                despesas_dicts = dados.get('despesas', [])

                # Convertendo os dicionários de receitas para instâncias de Receita
                self.receitas = [Receita(**receita.__dict__) for receita in dados.get('receitas', [])]
                
                # Convertendo os dicionários de despesas para instâncias de Despesa
                self.despesas = [Despesa(**despesa.__dict__) for despesa in dados.get('despesas', [])]

                # Limpar os conjuntos
                self.categorias_receita.clear()
                self.categorias_despesa.clear()

                # Adicionar as categorias ao conjunto
                for receita in self.receitas:
                    self.categorias_receita.add(receita.categoria)

                for despesa in self.despesas:
                    self.categorias_despesa.add(despesa.categoria)

    def salvar_dados(self):
        dados = {
            'receitas': self.receitas,
            'despesas': self.despesas
        }
        with open('dados.json', 'w') as arquivo_json:
            arquivo_json.write(jsonpickle.encode(dados))

    def __iter__(self):
        return iter(self.receitas + self.despesas)

# Instância do SistemaFinanceiro
sistema_financeiro = SistemaFinanceiro()
sistema_financeiro.carregar_dados()

# Rota para adicionar receitas
@app.route('/adicionar_receita', methods=['POST'])
def adicionar_receita():
    descricao = request.form.get('descricao_receita')
    valor_str = request.form.get('valor_receita')
    data = request.form.get('data_receita')
    categoria = request.form.get('categoria_receita')

    # Verifique se o valor foi fornecido antes de tentar convertê-lo
    if valor_str:
        valor = float(valor_str)
    else:
        # Se o valor não foi fornecido, você pode definir um valor padrão ou lidar com isso de outra forma.
        # Neste exemplo, estou definindo o valor como 0.0.
        valor = 0.0

    nova_receita = Receita(descricao=descricao, valor=valor, data=data, categoria=categoria)
    sistema_financeiro.adicionar_receita(nova_receita)
    salvar_dados()
    print(f"Receita adicionada: {descricao} - {valor} - {data} - {categoria}")
    return redirect(url_for('index'))

# Rota para adicionar despesas
@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    descricao = request.form.get('descricao_despesa')
    valor_str = request.form.get('valor_despesa')
    data = request.form.get('data_despesa')
    categoria = request.form.get('categoria_despesa')

    # Verifique se o valor foi fornecido antes de tentar convertê-lo
    if valor_str:
        valor = float(valor_str)
    else:
        # Se o valor não foi fornecido, você pode definir um valor padrão ou lidar com isso de outra forma.
        # Neste exemplo, estou definindo o valor como 0.0.
        valor = 0.0

    nova_despesa = Despesa(descricao=descricao, valor=valor, data=data, categoria=categoria)
    sistema_financeiro.adicionar_despesa(nova_despesa)
    salvar_dados()

    return redirect(url_for('index'))

# Função para salvar dados em um arquivo JSON
def salvar_dados():
    sistema_financeiro.salvar_dados()

# Função para carregar dados do arquivo JSON
def carregar_dados():
    if os.path.exists('dados.json'):
        with open('dados.json', 'r') as arquivo_json:
            dados = jsonpickle.decode(arquivo_json.read())

            sistema_financeiro.receitas = [Receita(**receita) for receita in dados.get('receitas', [])]
            sistema_financeiro.despesas = [Despesa(**despesa) for despesa in dados.get('despesas', [])]

            sistema_financeiro.categorias_receita = set()
            sistema_financeiro.categorias_despesa = set()

            for receita_dict in dados.get('receitas', []):
                sistema_financeiro.categorias_receita.add(receita_dict['categoria'])

            for despesa_dict in dados.get('despesas', []):
                sistema_financeiro.categorias_despesa.add(despesa_dict['categoria'])

# Rota para cadastrar nova categoria para despesa
@app.route('/cadastrar_categoria_despesa', methods=['POST'])
def cadastrar_categoria_despesa():
    nova_categoria = request.form.get('nova_categoria')
    cadastrar_nova_categoria(nova_categoria, 'despesa')
    return redirect(url_for('index'))

# Rota para cadastrar nova categoria para receita
@app.route('/cadastrar_categoria_receita', methods=['POST'])
def cadastrar_categoria_receita():
    nova_categoria = request.form.get('nova_categoria')
    cadastrar_nova_categoria(nova_categoria, 'receita')
    return redirect(url_for('index'))

# Função para cadastrar nova categoria
def cadastrar_nova_categoria(nova_categoria, tipo):
    if tipo == 'despesa':
        sistema_financeiro.categorias_despesa.add(nova_categoria)
    elif tipo == 'receita':
        sistema_financeiro.categorias_receita.add(nova_categoria)
    salvar_dados()

# Rota para acessar a tela de extrato mensal
@app.route('/extrato_mensal', methods=['POST'])
def extrato_mensal():
    mes_inicial = request.form.get('mes_inicial')
    mes_final = request.form.get('mes_final')

    # Validar e converter as datas para objetos datetime.date
    data_inicio = datetime.strptime(mes_inicial, '%Y-%m').date()
    data_fim = datetime.strptime(mes_final, '%Y-%m').date()

    extrato = obter_extrato_mensal(data_inicio, data_fim)

    return render_template('extrato_mensal.html', extrato=extrato)

# Função para obter o período do mês
def obter_periodo_mes(mes_extrato):
    data_inicio = datetime.strptime(mes_extrato, '%Y-%m').date().replace(day=1)
    
    if not isinstance(data_inicio, date):
        print(f"Data de início inválida: {data_inicio}")
        return None, None

    ultimo_dia_mes = monthrange(data_inicio.year, data_inicio.month)[1]
    data_fim = data_inicio.replace(day=ultimo_dia_mes)

    return data_inicio, data_fim

# Função para obter o extrato mensal
def obter_extrato_mensal(data_inicio, data_fim):
    extrato = {
        'meses': {},
        'total_receitas': 0,
        'total_despesas': 0
    }

    for dado in sistema_financeiro.receitas + sistema_financeiro.despesas:
        if isinstance(dado, Receita) or isinstance(dado, Despesa):
            if dado.data is None:
                # Se a data for None, ignore essa transação
                continue

            if isinstance(dado.data, str):
                # Se a data for uma string, converta para datetime.date
                dado.data = datetime.strptime(dado.data, '%Y-%m-%d').date()

            if data_inicio <= dado.data <= data_fim:
                mes = dado.data.strftime('%B %Y')  # Converter a data para uma string representando o mês e ano
                if mes not in extrato['meses']:
                    extrato['meses'][mes] = {'receitas': [], 'despesas': [], 'total_receitas': 0, 'total_despesas': 0, 'diferenca': 0}

                if isinstance(dado, Receita):
                    receita_dict = {
                        'descricao': dado.descricao,
                        'valor': dado.valor,
                        'data': dado.data.strftime('%Y-%m-%d'),
                        'categoria': dado.categoria
                    }
                    extrato['meses'][mes]['receitas'].append(receita_dict)
                    extrato['meses'][mes]['total_receitas'] += dado.valor
                    extrato['total_receitas'] += dado.valor
                elif isinstance(dado, Despesa):
                    despesa_dict = {
                        'descricao': dado.descricao,
                        'valor': dado.valor,
                        'data': dado.data.strftime('%Y-%m-%d'),
                        'categoria': dado.categoria
                    }
                    extrato['meses'][mes]['despesas'].append(despesa_dict)
                    extrato['meses'][mes]['total_despesas'] += dado.valor
                    extrato['total_despesas'] += dado.valor

    for mes, dados_mes in extrato['meses'].items():
        dados_mes['diferenca'] = dados_mes['total_receitas'] - dados_mes['total_despesas']

    return extrato


# Rota principal
@app.route('/')
def index():
    # Combine as listas de receitas e despesas
    todas_transacoes = sistema_financeiro.receitas + sistema_financeiro.despesas

    # Ordenar todas as transações com base na data em ordem decrescente
    todas_transacoes = sorted(todas_transacoes, key=lambda x: str(x.data), reverse=True)

    return render_template('index.html', sistema=todas_transacoes)



# Rota para exibir dados filtrados
@app.route('/filtrar_dados', methods=['POST'])
def filtrar_dados():
    categoria_filtro = request.form.get('categoria_filtro')
    data_filtro = request.form.get('data_filtro')
    descricao_filtro = request.form.get('descricao_filtro')

    dados_filtrados = filtrar_dados_por_categoria_data_descricao(
        sistema_financeiro.receitas + sistema_financeiro.despesas,
        categoria_filtro,
        data_filtro,
        descricao_filtro
    )

    sistema_filtrado = SistemaFinanceiro()

    for dado in dados_filtrados:
        if isinstance(dado, Receita):
            sistema_filtrado.adicionar_receita(dado)
        elif isinstance(dado, Despesa):
            sistema_filtrado.adicionar_despesa(dado)

    return render_template('index.html', sistema=sistema_filtrado)

# Função para filtrar dados
def filtrar_dados_por_categoria_data_descricao(dados, categoria, data, descricao):
    dados_filtrados = []

    for dado in dados:
        # Use jsonpickle para desserializar o objeto
        dado_obj = jsonpickle.decode(dado)

        if (
            (categoria is None or dado_obj.categoria == categoria) and
            (data is None or dado_obj.data == data) and
            (descricao is None or descricao.lower() in dado_obj.descricao.lower())
        ):
            dados_filtrados.append(dado_obj)

    return dados_filtrados

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
