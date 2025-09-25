from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

# --- LÓGICA DO BANCO DE DADOS ---

def conectar_bd():
    """Conecta ao banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect('manutencao.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manutencao_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            data_troca TEXT NOT NULL,
            km_troca INTEGER NOT NULL,
            km_proxima INTEGER NOT NULL,
            meses_proxima INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def carregar_itens():
    """Carrega todos os itens do banco de dados, sem filtro."""
    conn = None
    try:
        conn = sqlite3.connect('manutencao.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manutencao_itens")
        registros = cursor.fetchall()
        itens = []
        
        for reg in registros:
            id, nome, valor, data_troca_str, km_troca, km_proxima, meses_proxima = reg
            
            data_troca = datetime.datetime.strptime(data_troca_str, '%Y-%m-%d').date()
            proxima_troca_km_prevista = km_troca + km_proxima
            proxima_data = data_troca + datetime.timedelta(days=meses_proxima * 30)
            
            itens.append({
                'id': id,
                'nome': nome,
                'valor': valor,
                'data_troca': data_troca.strftime('%Y-%m-%d'),
                'km_troca': km_troca,
                'km_proxima': km_proxima,
                'meses_proxima': meses_proxima,
                'proxima_data_formatada': proxima_data.strftime('%d/%m/%Y'),
                'proxima_troca_km_prevista': proxima_troca_km_prevista,
                'proxima_data_iso': proxima_data.isoformat()
            })
        return itens
    finally:
        if conn:
            conn.close()

def adicionar_item(data):
    """Adiciona um novo item ao banco de dados."""
    conn = None
    try:
        conn = sqlite3.connect('manutencao.db')
        cursor = conn.cursor()
        nome = data['nome']
        valor = float(data['valor'])
        data_troca_str = data['data_troca']
        km_troca = int(data['km_troca'])
        km_proxima = int(data['km_proxima'])
        meses_proxima = int(data['meses_proxima'])
        
        cursor.execute(
            "INSERT INTO manutencao_itens (nome, valor, data_troca, km_troca, km_proxima, meses_proxima) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, valor, data_troca_str, km_troca, km_proxima, meses_proxima)
        )
        conn.commit()
        return True, "Item adicionado com sucesso!"
    except (ValueError, KeyError, sqlite3.Error) as e:
        return False, f"Erro ao adicionar item: {e}"
    finally:
        if conn:
            conn.close()

def remover_item(item_id):
    """Remove um item do banco de dados pelo seu ID."""
    conn = None
    try:
        conn = sqlite3.connect('manutencao.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM manutencao_itens WHERE id = ?", (item_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Item removido com sucesso!"
        else:
            return False, "Item não encontrado."
    except sqlite3.Error as e:
        return False, f"Erro ao remover item: {e}"
    finally:
        if conn:
            conn.close()

def editar_item(item_id, data):
    """Edita um item no banco de dados pelo seu ID."""
    conn = None
    try:
        conn = sqlite3.connect('manutencao.db')
        cursor = conn.cursor()
        nome = data['nome']
        valor = float(data['valor'])
        data_troca_str = data['data_troca']
        km_troca = int(data['km_troca'])
        km_proxima = int(data['km_proxima'])
        meses_proxima = int(data['meses_proxima'])
        
        cursor.execute(
            """
            UPDATE manutencao_itens
            SET nome = ?, valor = ?, data_troca = ?, km_troca = ?, km_proxima = ?, meses_proxima = ?
            WHERE id = ?
            """,
            (nome, valor, data_troca_str, km_troca, km_proxima, meses_proxima, item_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Item atualizado com sucesso!"
        else:
            return False, "Item não encontrado."
    except (ValueError, KeyError, sqlite3.Error) as e:
        return False, f"Erro ao atualizar item: {e}"
    finally:
        if conn:
            conn.close()

def gerar_relatorio():
    """Gera um relatório detalhado em um arquivo .txt na raiz do projeto."""
    itens = carregar_itens()
    relatorio_texto = "Relatório de Manutenção do Veículo\n"
    relatorio_texto += "-----------------------------------\n\n"
    
    total_gasto = 0
    
    if not itens:
        relatorio_texto += "Nenhum item de manutenção registrado."
    else:
        for item in itens:
            relatorio_texto += f"Item: {item['nome']}\n"
            relatorio_texto += f"  - Valor: R${item['valor']:.2f}\n"
            relatorio_texto += f"  - Data da Troca: {item['data_troca']}\n"
            relatorio_texto += f"  - KM da Troca: {item['km_troca']}\n"
            relatorio_texto += f"  - Próxima Troca (KM): {item['proxima_troca_km_prevista']}\n"
            relatorio_texto += f"  - Próxima Troca (Data): {item['proxima_data_formatada']}\n\n"
            total_gasto += item['valor']
        
        relatorio_texto += "-----------------------------------\n"
        relatorio_texto += f"Resumo:\n"
        relatorio_texto += f"  - Total de Itens: {len(itens)}\n"
        relatorio_texto += f"  - Gasto Total Acumulado: R${total_gasto:.2f}\n"

    try:
        with open("relatorio_manutencao.txt", "w") as f:
            f.write(relatorio_texto)
        return True, "Relatório gerado com sucesso!"
    except Exception as e:
        return False, f"Erro ao gerar relatório: {e}"

# --- APLICAÇÃO WEB COM FLASK ---

app = Flask(__name__)

@app.route('/')
def index():
    """Rota principal que serve o HTML da aplicação."""
    return render_template('index.html')

@app.route('/api/itens', methods=['GET', 'POST'])
def handle_itens():
    """
    Endpoint da API para manipular os itens de manutenção.
    - GET: Retorna todos os itens do banco de dados.
    - POST: Adiciona um novo item ao banco de dados.
    """
    if request.method == 'GET':
        itens = carregar_itens()
        return jsonify(itens)

    elif request.method == 'POST':
        data = request.json
        sucesso, mensagem = adicionar_item(data)
        if sucesso:
            return jsonify({'mensagem': mensagem}), 201
        else:
            return jsonify({'mensagem': mensagem}), 400

@app.route('/api/itens/<int:item_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_item(item_id):
    """
    Endpoint da API para manipular um item específico por ID.
    - GET: Retorna um único item.
    - PUT: Edita um item existente.
    - DELETE: Remove um item existente.
    """
    if request.method == 'GET':
        conn = None
        try:
            conn = sqlite3.connect('manutencao.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM manutencao_itens WHERE id = ?", (item_id,))
            reg = cursor.fetchone()
            if reg:
                id, nome, valor, data_troca, km_troca, km_proxima, meses_proxima = reg
                item = {
                    'id': id,
                    'nome': nome,
                    'valor': valor,
                    'data_troca': data_troca,
                    'km_troca': km_troca,
                    'km_proxima': km_proxima,
                    'meses_proxima': meses_proxima
                }
                return jsonify(item)
            else:
                return jsonify({'mensagem': 'Item não encontrado.'}), 404
        finally:
            if conn:
                conn.close()

    elif request.method == 'PUT':
        data = request.json
        sucesso, mensagem = editar_item(item_id, data)
        if sucesso:
            return jsonify({'mensagem': mensagem}), 200
        else:
            return jsonify({'mensagem': mensagem}), 404

    elif request.method == 'DELETE':
        sucesso, mensagem = remover_item(item_id)
        if sucesso:
            return jsonify({'mensagem': mensagem}), 200
        else:
            return jsonify({'mensagem': mensagem}), 404

@app.route('/api/relatorio', methods=['POST'])
def handle_relatorio():
    """Endpoint da API para gerar o relatório."""
    sucesso, mensagem = gerar_relatorio()
    if sucesso:
        return jsonify({'mensagem': mensagem}), 200
    else:
        return jsonify({'mensagem': mensagem}), 500

if __name__ == '__main__':
    conn, _ = conectar_bd()
    conn.close()
    app.run(debug=True)