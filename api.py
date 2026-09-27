from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route('/api/transferencias', methods=['GET'])
def obter_transferencias():
    try:
        # Tentativa de conexão isolada com timeout explícito
        conexao = mysql.connector.connect(
            host='mysql-150d98e8-versao01.e.aivencloud.com',
            port=10256,
            user='avnadmin',
            password='AVNS_Kf6_PfesQM62x0b-wyy',
            database='defaultdb',
            connection_timeout=5
        )
        cursor = conexao.cursor(dictionary=True)
        
        query = """
            SELECT 
                j.nome AS nome_jogador, 
                j.foto_url,
                c.nome AS nome_clube, 
                c.escudo_url,
                n.status AS status, 
                n.fonte_nome AS fonte_nome,
                n.data_publicacao AS Data
            FROM negociacoes n
            JOIN jogadores j ON n.jogador_id = j.id
            JOIN clubes c ON n.clube_interessado_id = c.id
            ORDER BY n.data_publicacao DESC
            LIMIT 50
        """
        cursor.execute(query)
        dados = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        return jsonify(dados), 200
        
    except Exception as e:
        # Se falhar, retorna o erro exato em JSON para vermos no browser
        return jsonify({"status": "erro", "detalhe": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API Online e Operacional!"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)