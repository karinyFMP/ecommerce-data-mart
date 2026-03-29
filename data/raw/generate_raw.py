import os
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================
fake = Faker("pt_BR")
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_CLIENTES = 5000
NUM_PRODUTOS = 300
NUM_PEDIDOS = 20000

DATA_INICIO = datetime(2020, 1, 1)
DATA_FIM = datetime(2026, 3, 29)

# =========================================================
# TIPO CLIENTE
# =========================================================
tipos_cliente = [
    {"id_tipo_cliente": 1, "tipo_cliente": "Novo"},
    {"id_tipo_cliente": 2, "tipo_cliente": "Recorrente"},
    {"id_tipo_cliente": 3, "tipo_cliente": "VIP"},
]

df_tipos_cliente = pd.DataFrame(tipos_cliente)
df_tipos_cliente.to_csv(f"{OUTPUT_DIR}/raw_tipo_cliente.csv", index=False)

# =========================================================
# CATEGORIAS
# =========================================================
categorias = [
    {"id_categoria": 1, "nome_categoria": "Eletrônicos"},
    {"id_categoria": 2, "nome_categoria": "Moda"},
    {"id_categoria": 3, "nome_categoria": "Casa"},
    {"id_categoria": 4, "nome_categoria": "Beleza"},
    {"id_categoria": 5, "nome_categoria": "Esporte"},
]

df_categorias = pd.DataFrame(categorias)
df_categorias.to_csv(f"{OUTPUT_DIR}/raw_categorias.csv", index=False)

# =========================================================
# LOCALIZAÇÕES (27 estados, 10 cidades por estado)
# =========================================================
localizacoes_brasil = {
    "AC": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira", "Tarauacá", "Feijó", "Brasileia", "Xapuri", "Plácido de Castro", "Mâncio Lima", "Senador Guiomard"],
    "AL": ["Maceió", "Arapiraca", "Palmeira dos Índios", "Rio Largo", "União dos Palmares", "Penedo", "São Miguel dos Campos", "Coruripe", "Delmiro Gouveia", "Marechal Deodoro"],
    "AP": ["Macapá", "Santana", "Laranjal do Jari", "Oiapoque", "Mazagão", "Porto Grande", "Tartarugalzinho", "Pedra Branca do Amapari", "Vitória do Jari", "Amapá"],
    "AM": ["Manaus", "Parintins", "Itacoatiara", "Manacapuru", "Coari", "Tefé", "Tabatinga", "Maués", "Humaitá", "Iranduba"],
    "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari", "Itabuna", "Juazeiro", "Lauro de Freitas", "Ilhéus", "Jequié", "Barreiras"],
    "CE": ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Maracanaú", "Sobral", "Crato", "Itapipoca", "Maranguape", "Iguatu", "Quixadá"],
    "DF": ["Brasília", "Taguatinga", "Ceilândia", "Samambaia", "Planaltina", "Gama", "Sobradinho", "Guará", "Recanto das Emas", "Santa Maria"],
    "ES": ["Vitória", "Vila Velha", "Serra", "Cariacica", "Linhares", "Colatina", "Guarapari", "São Mateus", "Aracruz", "Cachoeiro de Itapemirim"],
    "GO": ["Goiânia", "Aparecida de Goiânia", "Anápolis", "Rio Verde", "Luziânia", "Águas Lindas de Goiás", "Valparaíso de Goiás", "Trindade", "Formosa", "Senador Canedo"],
    "MA": ["São Luís", "Imperatriz", "Caxias", "Timon", "Codó", "Paço do Lumiar", "Açailândia", "Bacabal", "Balsas", "Santa Inês"],
    "MG": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora", "Betim", "Montes Claros", "Uberaba", "Governador Valadares", "Ipatinga", "Sete Lagoas"],
    "MS": ["Campo Grande", "Dourados", "Três Lagoas", "Corumbá", "Ponta Porã", "Naviraí", "Nova Andradina", "Sidrolândia", "Aquidauana", "Paranaíba"],
    "MT": ["Cuiabá", "Várzea Grande", "Rondonópolis", "Sinop", "Tangará da Serra", "Sorriso", "Cáceres", "Lucas do Rio Verde", "Primavera do Leste", "Barra do Garças"],
    "PA": ["Belém", "Ananindeua", "Santarém", "Marabá", "Parauapebas", "Castanhal", "Abaetetuba", "Cametá", "Bragança", "Altamira"],
    "PB": ["João Pessoa", "Campina Grande", "Santa Rita", "Patos", "Bayeux", "Sousa", "Cajazeiras", "Cabedelo", "Guarabira", "Sapé"],
    "PE": ["Recife", "Jaboatão dos Guararapes", "Olinda", "Caruaru", "Petrolina", "Paulista", "Cabo de Santo Agostinho", "Camaragibe", "Garanhuns", "Vitória de Santo Antão"],
    "PI": ["Teresina", "Parnaíba", "Picos", "Piripiri", "Floriano", "Campo Maior", "Barras", "União", "Altos", "Pedro II"],
    "PR": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa", "Cascavel", "São José dos Pinhais", "Foz do Iguaçu", "Colombo", "Guarapuava", "Paranaguá"],
    "RJ": ["Rio de Janeiro", "São Gonçalo", "Duque de Caxias", "Nova Iguaçu", "Niterói", "Belford Roxo", "Campos dos Goytacazes", "Petrópolis", "Volta Redonda", "Macaé"],
    "RN": ["Natal", "Mossoró", "Parnamirim", "São Gonçalo do Amarante", "Macaíba", "Ceará-Mirim", "Caicó", "Assu", "Currais Novos", "Nova Cruz"],
    "RO": ["Porto Velho", "Ji-Paraná", "Ariquemes", "Vilhena", "Cacoal", "Rolim de Moura", "Jaru", "Guajará-Mirim", "Machadinho d'Oeste", "Ouro Preto do Oeste"],
    "RR": ["Boa Vista", "Rorainópolis", "Caracaraí", "Alto Alegre", "Mucajaí", "Bonfim", "Cantá", "Pacaraima", "Normandia", "Iracema"],
    "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Canoas", "Santa Maria", "Gravataí", "Viamão", "Novo Hamburgo", "São Leopoldo", "Passo Fundo"],
    "SC": ["Florianópolis", "Joinville", "Blumenau", "São José", "Criciúma", "Chapecó", "Itajaí", "Jaraguá do Sul", "Lages", "Balneário Camboriú"],
    "SE": ["Aracaju", "Nossa Senhora do Socorro", "Lagarto", "Itabaiana", "São Cristóvão", "Estância", "Tobias Barreto", "Simão Dias", "Nossa Senhora da Glória", "Capela"],
    "SP": ["São Paulo", "Campinas", "Guarulhos", "São Bernardo do Campo", "Santo André", "Osasco", "Sorocaba", "Ribeirão Preto", "São José dos Campos", "Santos"],
    "TO": ["Palmas", "Araguaína", "Gurupi", "Porto Nacional", "Paraíso do Tocantins", "Colinas do Tocantins", "Guaraí", "Tocantinópolis", "Dianópolis", "Miracema do Tocantins"]
}

regioes = {
    "AC": "Norte", "AL": "Nordeste", "AP": "Norte", "AM": "Norte", "BA": "Nordeste",
    "CE": "Nordeste", "DF": "Centro-Oeste", "ES": "Sudeste", "GO": "Centro-Oeste",
    "MA": "Nordeste", "MG": "Sudeste", "MS": "Centro-Oeste", "MT": "Centro-Oeste",
    "PA": "Norte", "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "PR": "Sul",
    "RJ": "Sudeste", "RN": "Nordeste", "RO": "Norte", "RR": "Norte", "RS": "Sul",
    "SC": "Sul", "SE": "Nordeste", "SP": "Sudeste", "TO": "Norte"
}

localizacoes = []
id_localizacao = 1

for uf, cidades in localizacoes_brasil.items():
    for cidade in cidades:
        localizacoes.append({
            "id_localizacao": id_localizacao,
            "cidade": cidade,
            "estado": uf,
            "regiao": regioes[uf]
        })
        id_localizacao += 1

df_localizacoes = pd.DataFrame(localizacoes)
df_localizacoes.to_csv(f"{OUTPUT_DIR}/raw_localizacoes.csv", index=False)

# =========================================================
# CLIENTES
# =========================================================
clientes = []
ufs = list(localizacoes_brasil.keys())

for i in range(1, NUM_CLIENTES + 1):
    uf = random.choice(ufs)
    cidade = random.choice(localizacoes_brasil[uf])

    tipo_cliente = random.choices(
        [1, 2, 3],
        weights=[0.45, 0.40, 0.15],
        k=1
    )[0]

    clientes.append({
        "id_cliente": i,
        "nome_cliente": fake.name(),
        "cpf": fake.cpf(),
        "sexo": random.choice(["Masculino", "Feminino"]),
        "cidade": cidade,
        "estado": uf,
        "id_tipo_cliente": tipo_cliente
    })

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv(f"{OUTPUT_DIR}/raw_clientes.csv", index=False)

# =========================================================
# PRODUTOS
# =========================================================
produtos_por_categoria = {
    1: ["Smartphone", "Notebook", "Fone Bluetooth", "Teclado Mecânico", "Mouse Gamer", "Monitor", "Tablet", "Smartwatch", "Caixa de Som", "Carregador Portátil"],
    2: ["Camiseta Básica", "Calça Jeans", "Vestido Casual", "Tênis Esportivo", "Jaqueta", "Shorts", "Blusa Social", "Mochila", "Boné", "Relógio"],
    3: ["Cafeteira", "Liquidificador", "Panela Elétrica", "Jogo de Cama", "Toalha de Banho", "Aspirador", "Luminária", "Mesa Dobrável", "Cadeira Escritório", "Ventilador"],
    4: ["Perfume", "Shampoo", "Condicionador", "Hidratante", "Protetor Solar", "Kit Maquiagem", "Sabonete Facial", "Escova Secadora", "Óleo Capilar", "Creme Corporal"],
    5: ["Bicicleta", "Halter", "Tapete Yoga", "Bola de Futebol", "Tênis Corrida", "Mochila Esportiva", "Corda de Pular", "Luvas Academia", "Garrafa Térmica", "Faixa Elástica"]
}

produtos = []
for i in range(1, NUM_PRODUTOS + 1):
    id_categoria = random.randint(1, 5)
    nome_base = random.choice(produtos_por_categoria[id_categoria])
    nome_produto = f"{nome_base} {random.choice(['Premium', 'Plus', 'Max', 'Pro', 'Essencial', 'X'])}"

    faixa_preco = {
        1: (80, 5000),
        2: (30, 400),
        3: (40, 1500),
        4: (20, 350),
        5: (25, 3000)
    }

    preco = round(random.uniform(*faixa_preco[id_categoria]), 2)

    produtos.append({
        "id_produto": i,
        "nome_produto": nome_produto,
        "id_categoria": id_categoria,
        "preco_base": preco
    })

df_produtos = pd.DataFrame(produtos)
df_produtos.to_csv(f"{OUTPUT_DIR}/raw_produtos.csv", index=False)

# =========================================================
# PESOS DE ESTADOS (para distribuição mais realista)
# =========================================================
pesos_estados = {
    "SP": 18, "RJ": 9, "MG": 10, "BA": 7, "PR": 6, "RS": 6, "SC": 5, "GO": 4,
    "PE": 4, "CE": 4, "PA": 3, "MT": 2.5, "MS": 2, "ES": 2, "DF": 2.5, "AM": 2,
    "MA": 2, "PB": 1.8, "RN": 1.6, "PI": 1.5, "AL": 1.4, "SE": 1.2, "TO": 1.0,
    "RO": 1.0, "AC": 0.7, "AP": 0.7, "RR": 0.5
}

# Mapeia cidades por UF com peso maior para capitais
cidade_pesos = {}
for uf, cidades in localizacoes_brasil.items():
    pesos = [6] + [2] * (len(cidades) - 1)  # capital com peso maior
    cidade_pesos[uf] = list(zip(cidades, pesos))

# =========================================================
# PEDIDOS E ITENS
# =========================================================
pedidos = []
itens_pedido = []
id_item = 1

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Boleto"]
pesos_pagamento = [0.38, 0.37, 0.15, 0.10]

status_pedido = ["Entregue", "Enviado", "Pago", "Pendente", "Cancelado"]
pesos_status = [0.72, 0.10, 0.07, 0.06, 0.05]

produtos_df = pd.DataFrame(produtos)

for id_pedido in range(1, NUM_PEDIDOS + 1):
    cliente = random.choice(clientes)

    data_aleatoria = DATA_INICIO + timedelta(
        days=random.randint(0, (DATA_FIM - DATA_INICIO).days)
    )

    uf_escolhido = random.choices(
        list(pesos_estados.keys()),
        weights=list(pesos_estados.values()),
        k=1
    )[0]

    cidades_uf = cidade_pesos[uf_escolhido]
    cidade_escolhida = random.choices(
        [c[0] for c in cidades_uf],
        weights=[c[1] for c in cidades_uf],
        k=1
    )[0]

    id_local = df_localizacoes[
        (df_localizacoes["estado"] == uf_escolhido) &
        (df_localizacoes["cidade"] == cidade_escolhida)
    ]["id_localizacao"].values[0]

    pagamento = random.choices(formas_pagamento, weights=pesos_pagamento, k=1)[0]
    status = random.choices(status_pedido, weights=pesos_status, k=1)[0]

    desconto = round(random.choice([0, 0, 0, 5, 10, 15, 20, 25, 30]), 2)
    frete = round(random.uniform(8, 45), 2)

    num_itens = random.choices([1, 2, 3, 4, 5], weights=[0.42, 0.30, 0.16, 0.08, 0.04], k=1)[0]

    total_itens = 0

    produtos_escolhidos = produtos_df.sample(n=num_itens, replace=False)

    for _, prod in produtos_escolhidos.iterrows():
        quantidade = random.randint(1, 4)
        variacao_preco = random.uniform(0.90, 1.10)
        valor_unitario = round(prod["preco_base"] * variacao_preco, 2)
        valor_total_item = round(quantidade * valor_unitario, 2)
        total_itens += valor_total_item

        itens_pedido.append({
            "id_item": id_item,
            "id_pedido": id_pedido,
            "id_produto": int(prod["id_produto"]),
            "quantidade": quantidade,
            "valor_unitario": valor_unitario
        })
        id_item += 1

    valor_total = round(total_itens - desconto + frete, 2)
    if valor_total < 0:
        valor_total = round(total_itens + frete, 2)

    pedidos.append({
        "id_pedido": id_pedido,
        "id_cliente": cliente["id_cliente"],
        "data_pedido": data_aleatoria.strftime("%Y-%m-%d"),
        "forma_pagamento": pagamento,
        "status_pedido": status,
        "id_localizacao": int(id_local),
        "desconto": desconto,
        "frete": frete
    })

df_pedidos = pd.DataFrame(pedidos)
df_itens_pedido = pd.DataFrame(itens_pedido)

df_pedidos.to_csv(f"{OUTPUT_DIR}/raw_pedidos.csv", index=False)
df_itens_pedido.to_csv(f"{OUTPUT_DIR}/raw_itens_pedido.csv", index=False)

# =========================================================
# RESUMO
# =========================================================
print("Arquivos RAW gerados com sucesso!")
print(f"Clientes: {len(df_clientes)}")
print(f"Tipos de cliente: {len(df_tipos_cliente)}")
print(f"Categorias: {len(df_categorias)}")
print(f"Produtos: {len(df_produtos)}")
print(f"Localizações: {len(df_localizacoes)}")
print(f"Pedidos: {len(df_pedidos)}")
print(f"Itens de pedido: {len(df_itens_pedido)}")