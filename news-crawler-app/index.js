var express = require('express'),
	path = require('path'),
	news = require('./routes/news'),
	json2csv = require('nice-json2csv');

var bodyParser = require('body-parser')
var morgan = require('morgan')
var serveStatic = require('serve-static')

var app = express();

app.set('port', process.env.PORT || 3000);
app.use(morgan('dev')); /* 'default', 'short', 'tiny', 'dev' */
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(serveStatic(path.join(__dirname, 'public')));
app.use(json2csv.expressDecorator);

app.get('/news', news.findAll);
app.get('/news/count', news.countAll);
app.get('/news/export', news.exportNews);
app.get('/stats/1', news.stats1);
app.get('/stats/2', news.stats2);
app.get('/stats/3', news.stats3);
app.get('/stats/4', news.stats4);
app.get('/stats/5', news.stats5);

app.listen(app.get('port'), function () {
	console.log("Express server listening on port " + app.get('port'));
});
