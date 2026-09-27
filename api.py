from flask import Flask, render_template, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return mysql.connector.connect(
        host='mysql-150d98e8-versao01.e.aivencloud.com',
        port=10256,
        user='avnadmin',
        password='AVNS_Kf6_PfesQM62x0b-wyy',
        database='defaultdb'
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/transferencias')
def transferencias():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        # Consulta unindo as novas tabelas de jogadores, clubes e negociações
        query = """
            SELECT 
                j.nome AS Jogador,
                co.nome AS Origem,
                ci.nome AS Destino,
                n.status AS Status,
                n.fonte_nome AS Fonte,
                n.valor AS Valor
            FROM negociacoes n
            JOIN jogadores j ON n.jogador_id = j.id
            LEFT JOIN clubes co ON n.clube_origem_id = co.id
            LEFT JOIN clubes ci ON n.clube_interessado_id = ci.id
            ORDER BY n.id DESC
            LIMIT 50;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)