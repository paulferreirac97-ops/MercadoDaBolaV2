import os
import requests
import mysql.connector
from datetime import datetime
import time

def conectar_banco():
    try:
        return mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'mysql-150d98e8-versao01.e.aivencloud.com'), 
            port=int(os.environ.get('DB_PORT', 10256)),
            user=os.environ.get('DB_USER', 'avnadmin'), 
            password=os.environ.get('DB_PASSWORD'), 
            database=os.environ.get('DB_NAME', 'defaultdb')
        )
    except Exception as e:
        print(f"Erro crítico no banco: {e}")
        return None

def obter_ou_criar_clube(cursor, nome):
    cursor.execute("SELECT id FROM clubes WHERE nome = %s", (nome,))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]
    cursor.execute("INSERT INTO clubes (nome, escudo_url) VALUES (%s, %s)", (nome, "0"))
    return cursor.lastrowid

def obter_ou_criar_jogador(cursor, nome, posicao):
    cursor.execute("SELECT id, posicao FROM jogadores WHERE nome = %s", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        jogador_id, posicao_antiga = resultado
        if posicao_antiga == "A definir" and posicao != "A definir":
            cursor.execute("UPDATE jogadores SET posicao = %s WHERE id = %s", (posicao, jogador_id))
        return jogador_id
        
    cursor.execute("INSERT INTO jogadores (nome, foto_url, posicao) VALUES (%s, %s, %s)", (nome, "0", posicao))
    return cursor.lastrowid

def salvar_negociacao(conexao, jogador, clube_destino, clube_origem, valor, link_fonte, posicao, status, data_oficial):
    try:
        cursor = conexao.cursor()
        id_jogador = obter_ou_criar_jogador(cursor, jogador, posicao)
        id_destino = obter_ou_criar_clube(cursor, clube_destino)
        id_origem = obter_ou_criar_clube(cursor, clube_origem) if clube_origem and clube_origem != "Desconhecido" else None
        
        cursor.execute("SELECT id FROM negociacoes WHERE jogador_id = %s AND clube_interessado_id = %s AND status = %s", (id_jogador, id_destino, status))
        if cursor.fetchone(): return 
            
        query = """INSERT INTO negociacoes (jogador_id, clube_origem_id, clube_interessado_id, status, fonte_nome, url_noticia, data_publicacao, valor)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, (id_jogador, id_origem, id_destino, status, "365Scores", link_fonte, data_oficial, valor))
        conexao.commit()
        
        origem_txt = clube_origem if clube_origem else "---"
        print(f"[+] SALVO: {jogador} | {origem_txt} ➔ {clube_destino} | [{status}] em {data_oficial}")
    except Exception as e:
        conexao.rollback()
    finally:
        cursor.close()

def raspar_api_365(conexao):
    apis = {
        "SÉRIE A": "https://webws.365scores.com/web/transfers/?appTypeId=5&langId=31&timezoneName=America%2FSao_Paulo&userCountryId=21&competitions=113&limit=40",
        "SÉRIE B": "https://webws.365scores.com/web/transfers/?appTypeId=5&langId=31&timezoneName=America%2FSao_Paulo&userCountryId=21&competitions=116&limit=40"
    }
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

    for liga, url_api in apis.items():
        print(f"\n--- Consumindo API do 365Scores: {liga} ---")
        try:
            req = requests.get(url_api, headers=headers, timeout=10)
            dados = req.json()
            
            atletas = {a['id']: a.get('name', 'Desconhecido') for a in dados.get('athletes', [])}
            clubes = {c['id']: c.get('name', 'Desconhecido') for c in dados.get('competitors', [])}
            posicoes = {p['id']: p.get('name', 'A definir') for p in dados.get('positions', [])}
            
            for t in dados.get('transfers', []):
                try:
                    nome_jogador = atletas.get(t.get('athleteId'), 'Desconhecido')
                    posicao = posicoes.get(t.get('positionId'), 'A definir')
                    clube_origem = clubes.get(t.get('origin'), 'Desconhecido')
                    clube_destino = clubes.get(t.get('target'), 'Desconhecido')
                    
                    valor = t.get('price', '-')
                    if valor == "-": valor = "Não revelado"
                    
                    status_nome = str(t.get('statusName', '')).strip().title()
                    tipo_transferencia = t.get('transferType', {}).get('name', '')
                    
                    if status_nome.upper() == "RUMOR":
                        status = "Rumor"
                    else:
                        status = tipo_transferencia if tipo_transferencia else "Transferência"
                        
                    data_api_bruta = t.get('time', '')
                    if data_api_bruta:
                        data_oficial = data_api_bruta[:19].replace('T', ' ')
                    else:
                        data_oficial = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    link_id = "113" if liga == "SÉRIE A" else "116"
                    link_fonte = f"https://www.365scores.com/pt-br/football/league/brasileirao-{link_id}/transfers"
                    
                    salvar_negociacao(conexao, nome_jogador, clube_destino, clube_origem, valor, link_fonte, posicao, status, data_oficial)
                except Exception:
                    pass
        except Exception as e:
            print(f"Erro na requisição: {e}")
        time.sleep(2)

if __name__ == "__main__":
    print("Iniciando motor API JSON (365Scores)...")
    conn = conectar_banco()
    if conn:
        raspar_api_365(conn)
        conn.close()
        print("\n🏁 Banco de dados atualizado com sucesso!")