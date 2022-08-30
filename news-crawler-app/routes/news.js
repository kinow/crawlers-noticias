var neo4j = require('neo4j');
const pass = process.env.PASS;
var db = new neo4j.GraphDatabase('http://neo4j:' + pass + '@localhost:7474');

exports.findAll = function(req, res) {
    var perPage = 50;
    var skip = 0;

    // pagination
    var page = req.query.page;
    if (page) {
        skip = (page * perPage);
    }

    var queryParameters = buildQueryParameters(req);
    var where = createWhereParameter(queryParameters);

    var query = "MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) WITH n1, r1, n2 ORDER BY n1.date, n1.journal DESC " + where + " RETURN n1.url AS url1, n1.journal AS journal1, n1.title AS title1, n1.date AS date1, r1.token AS token, n2.url AS url2, n2.journal AS journal2, n2.title AS title2, n2.date AS date2 SKIP " + skip + " LIMIT " + perPage;
    console.log(query);
    db.query(query, params = {}, function(err, result) {
        res.send(result);
    });
};

exports.countAll = function(req, res) {
    var queryParameters = buildQueryParameters(req);
    var where = createWhereParameter(queryParameters);

    var query = "MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) " + where + "RETURN COUNT(n1.url) AS total";
    db.query(query, params = {}, function(err, result) {
        res.send(result[0]);
    });
};

exports.exportNews = function(req, res) {
    var queryParameters = buildQueryParameters(req);
    var where = createWhereParameter(queryParameters);

    var query = "MATCH (n1:News)-[r1:HAS_SAME_TOKEN]-(n2:News) " + where + " RETURN n1.url AS url1, n1.journal AS journal1, n1.title AS title1, n1.date AS date1, r1.token AS token, n2.url AS url2, n2.journal AS journal2, n2.title AS title2, n2.date AS date2 ORDER BY date1, journal1 DESC";
    db.query(query, params = {}, function(err, result) {
        res.csv(result, "news_export_"+ Date.now()+".csv");
    });
};

// Amount of journals
exports.stats1 = function(req, res) {
    var query = 'MATCH (n1:News) RETURN DISTINCT n1.journal, COUNT(*) AS total ORDER BY total DESC';
    db.query(query, params = {}, function(err, result) {
        res.send(result);
    });
};

// Amount of news
exports.stats2 = function(req, res) {
    var query = 'MATCH (n1:News) RETURN COUNT(*) AS total';
    db.query(query, params = {}, function(err, result) {
        res.send(result[0]);
    });
};

// Amount of news per journal
exports.stats3 = function(req, res) {
    var query = 'MATCH (n1:News) RETURN n1.journal, COUNT(n1) AS total ORDER BY total DESC';
    db.query(query, params = {}, function(err, result) {
        res.send(result);
    });
};

// Relationships among journals
exports.stats4 = function(req, res) {
    var query = 'MATCH (n1:News)-[r]-(n2:News) RETURN n1.journal, COUNT(n1) AS total, n2.journal ORDER BY n1.journal';
    db.query(query, params = {}, function(err, result) {
        res.send(result);
    });
};

// News per day per journal
exports.stats5 = function(req, res) {
    var query = 'MATCH (n1:News) RETURN n1.date AS date, n1.journal AS journal, COUNT(n1) AS total ORDER BY n1.journal, n1.date DESC';
    db.query(query, params = {}, function(err, result) {
        res.send(result);
    });
};

var buildQueryParameters = function(req) {
    var queryParams = new Object();
    if (req.query.journal1 && req.query.journal1.length > 0) {
        queryParams['n1.journal'] = req.query.journal1;
    }
    if (req.query.journal2 && req.query.journal2.length > 0) {
        queryParams['n2.journal'] = req.query.journal2;
    }
    if (req.query.date && req.query.date.length > 0) {
        queryParams['n1.date'] = req.query.date + ' 00:00:00';
    }
    return queryParams;
};

var createWhereParameter = function(queryParameters) {
    var where = '';
    var first = true;
    for (parameter in queryParameters) {
        var value = queryParameters[parameter];
        if (first) {
            where = where + ' WHERE ';
        } else {
            where = where + ' AND ';
        }
        where = where + " " + parameter + " = '" + value + "' ";
        first = false;
    }
    return where;
};
