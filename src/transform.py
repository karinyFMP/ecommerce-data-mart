import pandas as pd

def transform(data):
    # 1. DIMENSÃO CLIENTE (Consolidada e LGPD)
    df_clientes = data["clientes"].copy()
    df_tipos = data["tipo_cliente"].copy()
    dim_cliente = df_clientes.merge(df_tipos, on="id_tipo_cliente", how="left")
    dim_cliente["nome_cliente"] = dim_cliente["nome_cliente"].str.upper()
    dim_cliente["cpf"] = "***." + dim_cliente["cpf"].str[4:11] + "-**"
    dim_cliente = dim_cliente.drop(columns=["id_tipo_cliente"])

    # 2. DIMENSÃO PRODUTO (Consolidada)
    df_produtos = data["produtos"].copy()
    df_cats = data["categorias"].copy()
    dim_produto = df_produtos.merge(df_cats, on="id_categoria", how="left")
    dim_produto["nome_produto"] = dim_produto["nome_produto"].str.upper()
    dim_produto["preco_base"] = dim_produto["preco_base"].astype(float)
    dim_produto = dim_produto.drop(columns=["id_categoria"])

    # 3. DIMENSÃO LOCALIZAÇÃO
    dim_localizacao = data["localizacao"].copy()
    dim_localizacao["cidade"] = dim_localizacao["cidade"].str.strip()
    dim_localizacao = dim_localizacao.drop_duplicates()

    # 4. DIMENSÃO TEMPO (Rica em Detalhes e PT-BR)
    df_pedidos = data["pedidos"].copy()
    df_pedidos["data_pedido"] = pd.to_datetime(df_pedidos["data_pedido"])
    
    dim_tempo = pd.DataFrame({"data": df_pedidos["data_pedido"].unique()})
    dim_tempo = dim_tempo.sort_values("data") # Ordenar por data
    
    # Chaves e Datas Básicas
    dim_tempo["id_tempo"] = dim_tempo["data"].dt.strftime('%Y%m%d').astype(int)
    dim_tempo["ano"] = dim_tempo["data"].dt.year
    dim_tempo["mes_num"] = dim_tempo["data"].dt.month
    dim_tempo["dia"] = dim_tempo["data"].dt.day
    
    # Mapeamentos para Português
    meses_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    dias_pt = {
        "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
    }

    # Nomes dos Meses e Dias
    dim_tempo["nome_mes"] = dim_tempo["mes_num"].map(meses_pt)
    dim_tempo["nome_mes_abrev"] = dim_tempo["nome_mes"].str[:3] # Jan, Fev...
    dim_tempo["dia_semana"] = dim_tempo["data"].dt.day_name().map(dias_pt)
    
    # Trimestres Formatados
    dim_tempo["trimestre_num"] = dim_tempo["data"].dt.quarter
    dim_tempo["nome_trimestre"] = dim_tempo["trimestre_num"].apply(lambda x: f"{x}º Trimestre")
    
    # Colunas Auxiliares para Gráficos
    dim_tempo["mes_ano"] = dim_tempo["nome_mes_abrev"] + "/" + dim_tempo["ano"].astype(str)
    dim_tempo["fim_de_semana"] = dim_tempo["data"].dt.dayofweek.isin([5, 6]).map({True: "Sim", False: "Não"})

    # 5. FATO VENDAS (Métricas e Rateios)
    df_itens = data["itens"].copy()
    df_itens["valor_total_bruto"] = df_itens["quantidade"] * df_itens["valor_unitario"]
    
    total_pedido = df_itens.groupby("id_pedido")["valor_total_bruto"].sum().reset_index()
    total_pedido = total_pedido.rename(columns={"valor_total_bruto": "valor_total_produtos"})
    df_itens = df_itens.merge(total_pedido, on="id_pedido", how="left")
    
    df_itens["peso_item"] = df_itens["valor_total_bruto"] / df_itens["valor_total_produtos"]
    
    fato_vendas = df_itens.merge(df_pedidos, on="id_pedido", how="left")
    
    # Cálculos Financeiros
    fato_vendas["percentual_desconto"] = fato_vendas["desconto"] / 100.0
    fato_vendas["valor_desconto_item"] = fato_vendas["valor_total_bruto"] * fato_vendas["percentual_desconto"]
    fato_vendas["valor_liquido_item"] = fato_vendas["valor_total_bruto"] - fato_vendas["valor_desconto_item"]
    fato_vendas["frete_rateado"] = fato_vendas["frete"] * fato_vendas["peso_item"]
    
    # FK para a Dim_Tempo
    fato_vendas["fk_tempo"] = fato_vendas["data_pedido"].dt.strftime('%Y%m%d').astype(int)

    colunas_fato = [
        "id_pedido", "id_cliente", "id_produto", "id_localizacao", 
        "fk_tempo", "quantidade", "valor_unitario", "valor_total_bruto", 
        "percentual_desconto", "valor_desconto_item", "frete_rateado", 
        "valor_liquido_item", "status_pedido"
    ]

    return {
        "dim_cliente": dim_cliente,
        "dim_produto": dim_produto,
        "dim_localizacao": dim_localizacao,
        "dim_tempo": dim_tempo,
        "fato_vendas": fato_vendas[colunas_fato]
    }