# Crawlers de Notícias

Este projeto possui dois scripts *Python* principais. Um para **indexar notícias**, e outro
para buscar e gerar um banco de dados com **notícias que possuem termos iguais**.

A entrada de dados são arquivos *JSON*, gerados por **crawlers**. Nos arquivos há um array com
hashes contendo data, url, título, e o código do jornal (sbt para jornal do sbt, jn para
jornal nacional, etc.).

## Requisitos

- Python 2.x
- PyLucene (http://bendemott.blogspot.co.nz/2013/11/installing-pylucene-4-451.html)
  - JDK 1.7
  - python-dev
  - jcc (shipped with PyLucene)
- NLTK
- Neo4J

## Indexação

`index.sh`

Durante a indexação dos documentos, o script `index.sh` cria um `StandarAnalyzer` do *Lucene*.
Este tipo de *Analyzer* indexa tudo em minúsculas, quebrando em tokens usando o `StandardTokenizer`, 
e quando uma lista de stop-words é informada, ele também filtra por estas.

O script de indexação busca um arquivo chamado `stopwords.txt` no mesmo diretório de execução
para carregar em um `Set` todas as stop-words.

## Comparação

`relationships.sh`

No script de comparação, `relationships.sh` busca noticias em jornais diferentes para
a mesma data, gerando uma nova lista que e depois persistida em banco de dados.

## Visualização

É possível realizar queries no *Neo4J* para visualizar resultados no formato de grafos. Há também
uma ferramenta web, que sumariza e pagina os dados. Primeiro voce precisará carregar os dados gerados
pelo script `relationships.sh` no banco Neo4J, como indicado na próxima seção.

Por fim, inicializando a aplicação web, ela se conectará por padrão no servidor Neo4J rodando localmente, 
e poderá ser visualizada em <http://localhost:3000>.

## Reproduzindo os resultados

Caso você já tenha carregado dados na base, será necessário limpar o conteúdo do banco de dados primeiro.

```
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
DELETE n,r
```

O script `index.sh` produz um arquivo *CSV* `all.csv`, que possui o grafo com nós e atributos. é necessário
também criar um índice na URL, caso contrário as queries demorarão vários minutos.

(Primeiro, remova a configuração do Neo4j que impede o carregamento de CSVs de qualquer diretório)

```
LOAD CSV FROM 'file:///$PATH_TO_PROJECT/all.csv' AS line 
CREATE(:News { journal: line[0], date: line[1], url: line[2], title: line[3]})

CREATE INDEX ON :News(url)
```

Uma vez carregados, podemos criar os vértices do grafo. Os vértices estarão no arquivo `relationships.csv`, 
que é criado quando executamos o script `relationships.sh`.

```
LOAD CSV FROM 'file:///$PATH_TO_PROJECT/relationships.csv' AS line 
MATCH (n1:News) 
WHERE n1.url = line[0] // left 
MATCH (n2:News) 
WHERE n2.url = line[2] // right
MERGE (n1)-[r1:HAS_SAME_TOKEN {token: line[1]}]-(n2) 
```

Uma vez carregados os vértices, as seguintes queries servem para verificar o conteúdo no grafo.

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
