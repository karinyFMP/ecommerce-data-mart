-- 1. Qual é o faturamento total e a quantidade de itens vendidos por categoria de produto?
SELECT 
    p.nome_categoria,
    SUM(f.quantidade) AS total_itens_vendidos,
    SUM(f.valor_total_item) AS faturamento_total,
    ROUND(AVG(f.valor_total_item), 2) AS ticket_medio_item
FROM fato_vendas f
JOIN dim_produto p 
    ON f.id_produto = p.id_produto
WHERE f.status_pedido != 'Cancelado'
GROUP BY p.nome_categoria
ORDER BY faturamento_total DESC;


-- 2. Quem são os Top 10 Clientes em volume de compras e qual o seu perfil?
SELECT 
    c.nome_cliente,
    c.tipo_cliente,
    c.estado,
    COUNT(DISTINCT f.id_pedido) AS total_pedidos,
    SUM(f.valor_total_item) AS valor_total_gasto
FROM fato_vendas f
JOIN dim_cliente c 
    ON f.id_cliente = c.id_cliente
GROUP BY 
    c.id_cliente, 
    c.nome_cliente, 
    c.tipo_cliente, 
    c.estado
ORDER BY valor_total_gasto DESC
LIMIT 10;


-- 3. Como está distribuído o faturamento por Região e Estado no último ano?
SELECT 
    l.regiao,
    l.estado,
    SUM(f.valor_total_item) AS receita_bruta,
    COUNT(DISTINCT f.id_pedido) AS volume_pedidos
FROM fato_vendas f
JOIN dim_localizacao l 
    ON f.id_localizacao = l.id_localizacao
JOIN dim_tempo t 
    ON f.id_tempo = t.id_tempo
WHERE t.ano = 2025
GROUP BY 
    l.regiao, 
    l.estado
ORDER BY 
    l.regiao ASC, 
    receita_bruta DESC;


-- 4. Qual a evolução mensal das vendas e o impacto dos descontos ao longo do tempo?
SELECT 
    t.ano,
    t.mes,
    SUM(f.valor_total_item) AS faturamento_mensal,
    SUM(f.desconto) AS total_descontos,
    ROUND(
        (SUM(f.desconto) / SUM(f.valor_total_item)) * 100, 
        2
    ) AS percentual_desconto
FROM fato_vendas f
JOIN dim_tempo t 
    ON f.id_tempo = t.id_tempo
GROUP BY 
    t.ano, 
    t.mes
ORDER BY 
    t.ano ASC, 
    t.mes ASC;


-- 5. Qual a preferência de forma de pagamento de acordo com o Tipo de Cliente?
SELECT 
    c.tipo_cliente,
    f.forma_pagamento,
    COUNT(DISTINCT f.id_pedido) AS quantidade_pedidos,
    SUM(f.valor_total_item) AS volume_transacionado
FROM fato_vendas f
JOIN dim_cliente c 
    ON f.id_cliente = c.id_cliente
GROUP BY 
    c.tipo_cliente, 
    f.forma_pagamento
ORDER BY 
    c.tipo_cliente ASC, 
    volume_transacionado DESC;