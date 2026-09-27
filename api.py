import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

def conectar_banco():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'mysql-150d98e8-versao01.e.aivencloud.com'),
        port=int(os.environ.get('DB_PORT', 10256)),
        user=os.environ.get('DB_USER', 'avnadmin'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'defaultdb')
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/transferencias', methods=['GET'])
def get_transferencias():
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                j.nome AS Jogador, 
                coalesce(c_origem.nome, 'Sem Clube') AS Origem, 
                c_destino.nome AS Destino, 
                n.valor AS Valor, 
                n.status AS Status, 
                n.data_publicacao AS Data,
                n.fonte_nome AS Fonte
            FROM negociacoes n
            JOIN jogadores j ON n.jogador_id = j.id
            JOIN clubes c_destino ON n.clube_interessado_id = c_destino.id
            LEFT JOIN clubes c_origem ON n.clube_origem_id = c_origem.id
            ORDER BY n.data_publicacao DESC
            LIMIT 100
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        for row in resultados:
            if row['Data']:
                row['Data'] = row['Data'].strftime('%d/%m/%Y')
                
        cursor.close()
        conn.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)