# ecommerce-data-mart

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?logo=powerbi)

Este repositório contém o projeto final da disciplina de Banco de Dados/BI. Desenvolvemos um **Data Mart Dimensional completo** voltado para o setor de **E-commerce**, construindo um pipeline de dados que vai desde a extração de arquivos brutos (CSVs) até a visualização de insights em um dashboard interativo.


## 👥 Equipe

**Nome da Equipe:** ecommerce

**Integrantes:**
- Gabriel Alves de Oliveira
- Kariny Ferreira de Melo Picolotto
- Erika Francisca Augusto de Souza


## 📌 1. O Tema e Objetivo
Escolhemos o tema de **E-commerce** devido à sua riqueza em variáveis de análise. O objetivo principal deste Data Mart é permitir que gestores compreendam o comportamento de compras, a eficiência logística (prazos e fretes), a distribuição geográfica da receita e a performance do catálogo de produtos.

---

## 🏛️ 2. Modelagem Dimensional
O Data Mart foi estruturado seguindo o padrão **Star Schema**, garantindo alta performance para consultas analíticas.

* **Tabela Fato (`fato_vendas`):** A granularidade foi definida no nível do **Item do Pedido** (cada linha é um produto vendido dentro de um pedido). Isso permite análises detalhadas sem a necessidade de joins complexos entre múltiplas tabelas fato.
* **Tabelas de Dimensão:**
  * `dim_cliente`: Dados demográficos e perfil de compras (Novo, Recorrente, VIP).
  * `dim_produto`: Cadastro denormalizado contendo os nomes e as categorias.
  * `dim_localizacao`: Dados geográficos estruturados (Cidade, Estado, Região).
  * `dim_tempo`: Dimensão de calendário baseada na data do pedido (Smart Key: YYYYMMDD).

> 📄 **Dicionário de Dados:** A estrutura completa das tabelas, tipagens e chaves estrangeiras pode ser verificada no arquivo `schema.sql`.

---

## ⚙️ 3. Pipeline ETL e Qualidade de Dados
O processo de ETL (Extract, Transform, Load) foi orquestrado utilizando **Python** (biblioteca Pandas), com foco na limpeza e consistência:
1. **Extract:** Leitura de múltiplos arquivos `.csv` alocados na pasta `data/raw/`.
2. **Transform:** * Limpeza de strings (padronização para UPPERCASE para evitar duplicidades ocultas).
   * Conversão e tipagem correta de datas e valores monetários.
   * Junção das bases relacionais para a consolidação da Fato Única.
   * Criação de métricas de negócio pré-calculadas no processamento (ex: `valor_total_item`).
3. **Load:** Carga automatizada dos dados transformados no banco de dados **SQLite** (`ecommerce.db`).

---

## 🚀 4. Como Executar o Projeto (Passo a Passo)

Para garantir a reprodutibilidade deste projeto, siga o roteiro abaixo. Todo o processo foi desenhado para ser executado de forma simples no **VS Code**.


### 🛠️ Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
* **Python 3.8** ou superior.
* **VS Code** com a extensão **SQLite** instalada (pesquise por `alexcvzz.vscode-sqlite` nas extensões).
* **Power BI Desktop** (para visualizar o dashboard).

### Estrutura de Pastas
O código utiliza caminhos relativos (os.path.abspath), então a organização dos arquivos é fundamental. Certifique-se de que seu projeto siga este layout:
```bash
ecommerce-data-mart/
├── bin/                     <-- Scripts executáveis ou auxiliares
├── dashboards/              <-- Arquivos de visualização (ex: Power BI / E-Commerce.pbix)
├── data/                    <-- Diretório central de dados
│   ├── db/                  <-- Onde o banco SQLite (ecommerce.db) será criado
│   ├── parquet/             <-- Onde os arquivos Parquet serão salvos
│   └── raw/                 <-- Arquivos CSV originais brutos
├── docs/                    <-- Documentações adicionais do projeto
├── sql/                     <-- O Dump SQL (dump_ecommerce.sql) e outros scripts SQL ficam aqui
├── src/                     <-- Código-fonte do pipeline ETL
│   ├── extract.py
│   ├── gerar_dump.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── .gitignore               <-- Arquivo de exclusão de versionamento do Git
├── README.md                <-- Documentação principal do projeto
└── requirements.txt         <-- Lista de dependências (ex: pandas, pyarrow)
```

### Passo 1: Download do Projeto e Instalação de Dependências
Abra o terminal do VS Code, clone o projetos e instale as dependências:

```bash
# Clone o repositório
git clone https://github.com/karinyFMP/ecommerce-data-mart.git

# Acesse a pasta do projeto
cd ecommerce-data-mart

# Instale as dependências necessárias
pip install -r requirements.txt
```

### Passo 2: Executar o Pipeline (ETL)
Com o terminal aberto na raiz do projeto, execute o script principal. Ele fará a leitura dos CSVs brutos, aplicará as regras de negócio e criará o banco de dados do zero.
Para rodar o processo completo:

**Opção 1: Pelo botão "Play" (Mais fácil no VS Code)**
1. Na barra lateral esquerda, abra a pasta `src` e clique no arquivo `pipeline.py`.
2. Com o arquivo aberto, clique no botão de **"Play" (Run Python File)**, localizado no canto superior direito da tela do seu editor.

**Opção 2: Pelo Terminal (Linha de Comando)**
1. Abra o terminal ou prompt de comando na raiz do projeto.
2. Execute o seguinte comando:
```bash
python src/pipeline.py
```

O que acontece nesta etapa:

- Extract: O script lê os 7 arquivos CSV da pasta data/raw.

- Transform: O Pandas limpa os dados, mascara o CPF (LGPD), traduz datas para português e calcula métricas financeiras (frete rateado, descontos, etc.).

- Load: Cria o banco ecommerce.db e exporta as tabelas finais para a pasta data/parquet.
Se a execução for bem-sucedida, o arquivo ecommerce.db aparecerá na pasta do projeto.

### Passo 3: Validar os Dados no VS Code (Via Extensão)
Para provar que o banco foi populado corretamente sem sair do editor de código:

1. Pressione Ctrl + Shift + P (ou Cmd + Shift + P no Mac) para abrir a Paleta de Comandos.

2. Digite SQLite: Open Database e pressione Enter.

3. Selecione o arquivo recém-criado: ecommerce.db.

4. Observe a aba lateral inferior esquerda (SQLite Explorer). Clique nela para expandir e visualizar as tabelas (fato_vendas, dim_cliente, etc.). Clique no botão de "Play" ao lado de uma tabela para ver os dados nela contidos.

5. Método Alternativo (Terminal CLI): Caso prefira validar usando comandos SQL via terminal Windows (PowerShell), aponte para o executável do SQLite informando o caminho do banco:
```bash
PowerShell
& "D:\Caminho\Para\Seu\ecommerce-data-mart\bin\sqlite3.exe" ecommerce.db
```

### Passo 4: Restaurar o Banco de Dados via Dump (Backup)
Caso ocorra algum problema na execução do Python e você deseje apenas testar as queries SQL, disponibilizamos um arquivo de Dump com os dados já populados:

**Opção 1: Pelo botão "Play" (Mais fácil no VS Code)**
1. Na barra lateral esquerda, abra a pasta `src` e clique no arquivo `gerar_dump.py`.
2. Com o arquivo aberto, clique no botão de **"Play" (Run Python File)**, localizado no canto superior direito da tela do seu editor.

**Opção 2: Pelo Terminal (Linha de Comando)**
1. Abra o terminal ou prompt de comando na raiz do projeto.
2. Execute o seguinte comando:
```bash
python src/gerar_dump.py
```

### 5. Perguntas de Negócio e Insights
Nosso Data Mart nos permitiu responder a perguntas cruciais para o negócio. As queries SQL completas e documentadas estão no arquivo query.sql.

Qual é o faturamento total e a quantidade de itens vendidos por categoria de produto?

Quem são os Top 10 Clientes em volume de compras e qual o seu perfil?

Como está distribuído o faturamento por Região e Estado no último ano?

Qual a evolução mensal das vendas e o impacto financeiro dos descontos ao longo do tempo?

Qual a preferência de forma de pagamento de acordo com o Tipo de Cliente?

### 6. Dashboard (Power BI)
O arquivo E-Commerce.pbix contém a camada visual do projeto, conectada diretamente ao banco ecommerce.db via ODBC / Script Python.

Principais Visualizações:

Análise Temporal: Linhas indicando evolução de receita.

Mapa Geográfico: Heatmap de vendas por Estado, indicando os pólos logísticos.

Composição de Receita: Gráficos de barras rankeando categorias de produtos.
