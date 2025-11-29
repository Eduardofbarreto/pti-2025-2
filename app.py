from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy # Importando a ferramenta do Banco

app = Flask(__name__)
# ROTA PRINCIPAL: Quando acessar o site, mostra o HTML do seu amigo
@app.route('/')
def home():
    return render_template('index.html')

CORS(app)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expresso.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- A TABELA (O Molde dos Dados) ---
# Aqui definimos as colunas do Excel/Banco
class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Crachá único (1, 2, 3...)
    nome = db.Column(db.String(100))             # Nome do passageiro
    destino = db.Column(db.String(50))           # Para onde ele vai

# --- CRIA O BANCO ---
# Esse comando cria o arquivo .db se ele não existir
with app.app_context():
    db.create_all()

# --- ROTAS ---

@app.route('/comprar-passagem', methods=['POST'])
def comprar():
    dados = request.json
    
    # Criando uma nova linha na tabela
    nova_venda = Venda(nome=dados.get('nome'), destino=dados.get('destino'))
    
    # Salvando no banco de verdade
    db.session.add(nova_venda)
    db.session.commit() # O "Confirmar" final
    
    print(f"💰 Venda salva no Banco de Dados! ID: {nova_venda.id}")
    
    return jsonify({"mensagem": "Salvo no banco com sucesso!", "id": nova_venda.id})

@app.route('/ver-vendas', methods=['GET'])
def ver_vendas():
    # Vai no banco e pega TODAS as vendas
    todas_as_vendas = Venda.query.all()
    
    # Converte do formato do Banco para JSON (Lista)
    lista_de_vendas = []
    for venda in todas_as_vendas:
        lista_de_vendas.append({
            "id": venda.id,
            "nome": venda.nome,
            "destino": venda.destino
        })
        
    return jsonify(lista_de_vendas)

if __name__ == '__main__':
    print("🚀 Servidor com Banco de Dados SQLite rodando!")
    app.run(port=5000, debug=True)
