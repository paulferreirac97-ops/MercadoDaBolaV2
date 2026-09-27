import os
import mysql.connector

print("A ligar ao novo MySQL na Aiven...")

try:
    conexao = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'mysql-150d98e8-versao01.e.aivencloud.com'),
        port=int(os.environ.get('DB_PORT', 10256)),
        user=os.environ.get('DB_USER', 'avnadmin'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'defaultdb'),
        connect_timeout=10,
        autocommit=True
    )
    cursor = conexao.cursor()

    print("Desligando verificações de chave estrangeira...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    print("A limpar eventuais tabelas antigas...")
    cursor.execute("DROP TABLE IF EXISTS negociacoes;")
    cursor.execute("DROP TABLE IF EXISTS jogadores;")
    cursor.execute("DROP TABLE IF EXISTS clubes;")

    print("A criar novas tabelas estruturadas...")
    
    cursor.execute("""
        CREATE TABLE clubes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL UNIQUE,
            escudo_url TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE jogadores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL UNIQUE,
            foto_url TEXT,
            posicao VARCHAR(100)
        );
    """)

    cursor.execute("""
        CREATE TABLE negociacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jogador_id INT,
            clube_origem_id INT,
            clube_interessado_id INT,
            status VARCHAR(50),
            fonte_nome VARCHAR(100),
            url_noticia TEXT,
            data_publicacao DATETIME,
            valor VARCHAR(100),
            FOREIGN KEY (jogador_id) REFERENCES jogadores(id),
            FOREIGN KEY (clube_origem_id) REFERENCES clubes(id),
            FOREIGN KEY (clube_interessado_id) REFERENCES clubes(id)
        );
    """)

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("✅ Sucesso absoluto! O novo banco foi configurado instantaneamente.")

except Exception as e:
    print(f"❌ Erro ao configurar o banco: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conexao' in locals() and conexao.is_connected(): conexao.close()