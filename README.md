# Crawlers de Noticias

Este projeto possui dois programas Python principais. Um para indexar noticias, e outro
para buscar e gerar um banco de dados com noticias que possuem termos iguais.

A entrada de dados sao arquivos JSON, gerados por crawlers. Nos arquivos ha um array com
hashes contendo data, url, titulo, e o codigo do jornal (sbt para jornal do sbt, jn para
jornal nacional, etc).

## Requisitos

- Python 2.x
- PyLucene (http://bendemott.blogspot.co.nz/2013/11/installing-pylucene-4-451.html)
  - JDK 1.7
  - python-dev
  - jcc (shipped with PyLucene)
- NLTK
- Neo4J

## Indexacao

`index.sh`

Durante a indexacao dos documentos, o script cria um StandarAnalyzer do Lucene. Este tipo
de Analyzer a) indexa tudo em minusculas, quebrando em tokens usando o StandardTokenizer, 
e quando uma lista de stop words e informada, ele tambem filtra por elas.

O script de indexacao busca um arquivo chamado stopwords.txt no mesmo diretorio de execucao
para carregar em um Set todas as stop words.

## Comparacao

`relationships.sh`

No script de comparacao, ele busca noticias em jornais diferentes para a mesma data. Gerando
uma nova lista que e depois persistida em banco de dados.

## Visualizacao

E possivel realizar queries no Neo4J para visualizar resultados no formato de grafos. Ha tambem
uma ferramenta web, que sumariza e pagina os dados. Primeiro voce precisara carregar os dados gerados
pelo script relationships.sh no banco Neo4J, como indicado na proxima secao.

Por fim, inicializando a aplicacao web, ela se conectara por padrao no servidor Neo4J rodando localmente, 
e estara disponvel em http://localhost:3000.

## Reproduzindo os resultados

Caso voce ja tenha carregado dados na base, sera necessario limpar o conteudo do banco de dados primeiro.

```
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
DELETE n,r
```

O script index.sh produz um arquivo CSV all.csv, que possui o grafo com nos e atributos. E necessario
tambem criar um indice na URL, caso contrario as queries demorarao varios minutos.

```
LOAD CSV FROM 'file:///$PATH_TO_PROJECT/all.csv' AS line 
CREATE(:News { journal: line[0], date: line[1], url: line[2], title: line[3]})

CREATE INDEX ON :News(url)
```

Uma vez carregados, podemos criar os vertices do grafo. Os vertices estao no arquivo relationships.csv, 
que e criado quando executamos o script relationships.sh.

```
LOAD CSV FROM 'file:///$PATH_TO_PROJECT/relationships.csv' AS line 
MATCH (n1:News) 
WHERE n1.url = line[0] // left 
MATCH (n2:News) 
WHERE n2.url = line[2] // right
MERGE (n1)-[r1:HAS_SAME_TOKEN {token: line[1]}]-(n2) 
```

Uma vez carregados os vertices, as seguintes queries servem para verificar o conteudo no grafo.

```
# todas as noticias com tokens em comum
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) RETURN r1 
```

```
# Todas as noticias com tokens em comum, onde um dos jornais e o SBT
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) WHERE n1.journal = 'sbt' RETURN n1.url, n1.title, r1.token, n2.url, n2.title
```

```
# Todas as noticias com tokens em comum, onde um dos jornais e o JN
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) WHERE n1.journal = 'jn' RETURN n1.url, n1.title, r1.token, n2.url, n2.title
```
