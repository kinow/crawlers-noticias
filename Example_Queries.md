# Example Queries

* Query for the landing page

```
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) 
RETURN 
    n1.url,
    n1.journal, 
    n1.title,
    r1.token,
    n2.url,
    n2.journal, 
    n2.title,
    n1.date 
ORDER BY
    n2.date,
    n2.journal DESC 
LIMIT 50
```

## Queries with filters

* With the date filter

```
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) 
WHERE 
    n1.date = '2014-12-01 00:00:00'
RETURN 
    n1.url,
    n1.journal, 
    n1.title,
    r1.token,
    n2.url,
    n2.journal, 
    n2.title,
    n1.date 
SKIP 0 
LIMIT 50
```

* With the term filter

```
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) 
WHERE 
    r1.token = 'brasil'
RETURN 
    n1.url,
    n1.journal, 
    n1.title,
    r1.token,
    n2.url,
    n2.journal, 
    n2.title,
    n1.date 
SKIP 0 
LIMIT 50
```

* With the journal filter

```
MATCH (n1:News)-[r1:HAS_SAME_TOKEN]->(n2:News) 
WHERE 
    n1.journal = 'vcnog1' AND
    n2.journal = 'sbt' 
RETURN 
    n1.url,
    n1.journal, 
    n1.title,
    r1.token,
    n2.url,
    n2.journal, 
    n2.title,
    n1.date 
SKIP 0 
LIMIT 50
```

# Stats

* Amount of journals

```
MATCH (n1:News) RETURN DISTINCT n1.journal
```

* Amount of news

```
MATCH (n1:News) RETURN COUNT(*) AS TOTAL
```

* Amount of news per journal

```
MATCH (n1:News) RETURN n1.journal, COUNT(n1) AS TOTAL ORDER BY TOTAL DESC
```

* Relationships among journals

```
MATCH (n1:News)-[r]-(n2:News) RETURN n1.journal, COUNT(n1) AS TOTAL, n2.journal ORDER BY n1.journal 
```

* Summarise per day per journal

```
match (n1:News) where n1.journal = 'band' return count(n1), n1.date order by n1.date
```
