from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # Permite que o front-end (HTML/JS) comunique com esta API sem bloqueios de segurança

@app.route('/api/transferencias', methods=['GET'])
def obter_transferencias():
    try:
        conexao = mysql.connector.connect(
            host='mysql-150d98e8-versao01.e.aivencloud.com',
            port=10256,
            user='avnadmin',
            password='AVNS_Kf6_PfesQM62x0b-wyy',
            database='defaultdb'
        )
        cursor = conexao.cursor(dictionary=True)
        
        # Filtro exclusivo para o 365Scores
        query = """
            SELECT 
                j.nome AS Jogador, 
                j.foto_url,
                c.nome AS Clube, 
                c.escudo_url,
                n.status AS Status, 
                n.data_publicacao AS Data
            FROM negociacoes n
            JOIN jogadores j ON n.jogador_id = j.id
            JOIN clubes c ON n.clube_interessado_id = c.id
            WHERE n.fonte_nome = '365Scores'
            ORDER BY n.data_publicacao DESC
        """
        cursor.execute(query)
        dados = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        return jsonify(dados)
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)