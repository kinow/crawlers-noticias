# Crawlers de Noticias

Este projeto possui dois programas Python principais. Um para indexar noticias, e outro
para buscar e gerar um banco de dados com noticias que possuem termos iguais.

A entrada de dados sao arquivos JSON, gerados por crawlers. Nos arquivos ha um array com
hashes contendo data, url, titulo, e o codigo do jornal (sbt para jornal do sbt, jn para
jornal nacional, etc).

## Indexacao

Durante a indexacao dos documentos, o script cria um StandarAnalyzer do Lucene. Este tipo
de Analyzer a) indexa tudo em minusculas, quebrando em tokens usando o StandardTokenizer, 
e quando uma lista de stop words e informada, ele tambem filtra por elas.

O script de indexacao busca um arquivo chamado stopwords.txt no mesmo diretorio de execucao
para carregar em um Set todas as stop words.

## Comparacao

No script de comparacao, ele busca noticias em jornais diferentes para a mesma data. Gerando
uma nova lista que e depois persistida em banco de dados.

## Visualizacao

## Reproduzindo os resultados

### Criando base de grafo

MATCH (n)
OPTIONAL MATCH (n)-[r]-()
DELETE n,r

LOAD CSV FROM 'file:///home/kinow/Development/python/workspace/claudia-crawlers/all.csv' AS line 
CREATE(:News { journal: line[0], date: line[1], url: line[2], title: line[3]})

CREATE INDEX ON :News(url)

LOAD CSV FROM 'file:///home/kinow/Development/python/workspace/claudia-crawlers/relationships.csv' AS line 
MATCH (n1:News) 
WHERE n1.url = line[0] // left 
MATCH (n2:News) 
WHERE n2.url = line[2] // right
MERGE (n1)-[r1:HAS_SAME_TOKEN {token: line[1]}]-(n2) 

MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) RETURN r1 

MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) WHERE n1.journal = 'sbt' RETURN n1.url, n1.title, r1.token, n2.url, n2.title;

MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) WHERE n1.journal = 'jn' RETURN n1.url, n1.title, r1.token, n2.url, n2.title;
