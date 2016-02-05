var AppRouter = Backbone.Router.extend({

  routes: {
    "": "list",
    "news": "list",
    "stats": "stats"
  },

  initialize: function() {
    this.headerView = new HeaderView();
    $('#header').html(this.headerView.el);
  },

  list: function(params) {
    var newsList = new NewsCollection();
    var newsCounter = new NewsCounter();

    var url = '';
    var paramsList = buildQueryParameters(params);
    var first = true;
    for (param in paramsList) {
      var value = paramsList[param];
      if (first) {
        url = url + '?' + param + '=' + value;
        first = false;
      } else {
        url = url + '&' + param + '=' + value;
      }
    }
    newsList.url = '/news' + url;
    newsCounter.url = '/news/count' + url;
    // Display a loading indication whenever the Collection is fetching.
    newsCounter.bind("fetch", function() {
      $("#loading").modal();
      //this.html("<img src='/assets/img/spinner.gif'>");
    }, this);
    newsCounter.fetch({
      success: function() {
        var newsCount = newsCounter.attributes.total;
        newsList.fetch({
          success: function() {
            $("#loading").modal('hide');
            $("#content").html(new HomeView({
              model: newsList,
              newsCount: newsCount,
              params: params
            }).el);
          }
        });
      }
    });

    this.headerView.selectMenuItem('home-menu');
  },

  stats: function() {
    if (!this.statsView) {
      this.statsView = new StatsView();
    }
    $('#content').html(this.statsView.el);

    this.headerView.selectMenuItem('stats-menu');
  }

});

utils.loadTemplate(['HeaderView', 'FilterView', 'NewsItemView', 'Stats1View', 'Stats2View', 'Stats3View', 'Stats4View', 'Stats5View'], function() {
  app = new AppRouter();
  Backbone.history.start();
});

var buildQueryParameters = function(params) {
  var queryParams = new Object();
  if (!params)
    return queryParams;
  if (params.journal1 && params.journal1.length > 0) {
    queryParams['journal1'] = params.journal1;
  }
  if (params.journal2 && params.journal2.length > 0) {
    queryParams['journal2'] = params.journal2;
  }
  if (params.date && params.date.length > 0) {
    queryParams['date'] = params.date;
  }
  if (params.page && params.page.length > 0) {
    var page = parseInt(params.page, 10);
    if (page > 1) {
      queryParams['page'] = page;
    }
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
