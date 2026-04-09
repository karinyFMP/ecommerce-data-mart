import sqlite3
import os

def gerar_dump_sql():
    print("Iniciando a geração do Dump SQL...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "db", "ecommerce.db")
    
    # Conecta ao seu banco de dados populado
    conn = sqlite3.connect(db_path)
    
    # Cria/Abre um arquivo chamado 'dump_ecommerce.sql' para escrita na pasta sql
    caminho_dump = os.path.join(base_dir, "sql", "dump_ecommerce.sql")
    with open(caminho_dump, 'w', encoding='utf-8') as f:
        # A função iterdump() do SQLite gera todos os comandos SQL (DDL e DML)
        for linha in conn.iterdump():
            f.write(f"{linha}\n")
            
    conn.close()
    print(f"Dump SQL gerado com sucesso! Arquivo salvo em: {caminho_dump}")

if __name__ == "__main__":
    gerar_dump_sql()