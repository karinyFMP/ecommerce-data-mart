import pandas as pd
import os

def extract():
    data = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")

    data["clientes"] = pd.read_csv(os.path.join(raw_dir, "raw_clientes.csv"))
    data["produtos"] = pd.read_csv(os.path.join(raw_dir, "raw_produtos.csv"))
    data["pedidos"] = pd.read_csv(os.path.join(raw_dir, "raw_pedidos.csv"))
    data["itens"] = pd.read_csv(os.path.join(raw_dir, "raw_itens_pedido.csv"))
    data["localizacao"] = pd.read_csv(os.path.join(raw_dir, "raw_localizacoes.csv"))
    data["tipo_cliente"] = pd.read_csv(os.path.join(raw_dir, "raw_tipo_cliente.csv"))
    data["categorias"] = pd.read_csv(os.path.join(raw_dir, "raw_categorias.csv"))

    return data