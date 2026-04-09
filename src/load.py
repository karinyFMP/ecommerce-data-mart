import sqlite3
import os

def load(data):
    # Define o diretório base do projeto (raiz)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Gerenciamento da pasta do Banco de Dados SQLite
    db_dir = os.path.join(base_dir, "data", "db")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, "ecommerce.db")
    
    # 2. Gerenciamento da pasta Parquet (ideal para Power BI)
    parquet_dir = os.path.join(base_dir, "data", "parquet")
    if not os.path.exists(parquet_dir):
        os.makedirs(parquet_dir)
    
    # Conexão com SQLite
    conn = sqlite3.connect(db_path)

    for nome_tabela, df in data.items():
        # Carga no SQLite (mantém compatibilidade)
        df.to_sql(nome_tabela, conn, if_exists="replace", index=False)
        
        # Carga em formato Parquet (otimizado para BI)
        parquet_file_path = os.path.join(parquet_dir, f"{nome_tabela}.parquet")
        df.to_parquet(parquet_file_path, index=False)
        
        print(f"Sucesso: Tabela '{nome_tabela}' salva no DB e em Parquet.")

    conn.close()