from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def conectar_banco():
    return mysql.connector.connect(
        host='mysql-150d98e8-versao01.e.aivencloud.com', 
        port=10256,
        user='avnadmin', 
        password='AVNS_Kf6_PfesQM62x0b-wyy', 
        database='defaultdb',
        connect_timeout=5
    )

@app.route('/')
def home():
    return jsonify({"status": "API Online e Operacional!"})

@app.route('/api/transferencias', methods=['GET'])
def listar_transferencias():
    conexao = None
    cursor = None
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        # Consulta ultra-rápida trazendo apenas os campos essenciais com limite seguro
        query = """
            SELECT 
                j.nome AS nome_jogador,
                j.foto_url,
                j.posicao,
                c.nome AS nome_clube,
                c.escudo_url,
                n.status,
                n.fonte_nome,
                n.valor,
                n.data_publicacao
            FROM negociacoes n
            JOIN jogadores j ON n.jogador_id = j.id
            JOIN clubes c ON n.clube_interessado_id = c.id
            ORDER BY n.id DESC
            LIMIT 20;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
        
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)