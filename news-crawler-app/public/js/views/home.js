window.HomeView = Backbone.View.extend({

    initialize:function (params) {
        if (!params.params) {
            params.params = new Object();
            params.params.page = 1;
        }
        this.filterView = new FilterView({page: params.params.page, journal1: params.params.journal1, journal2: params.params.journal2, date: params.params.date});
        $(this.el).append(this.filterView.el);
        this.newsCount = params.newsCount;
        this.page = 1;
        if (params.params && params.params.page && params.params.page.length > 0) {
            this.page = parseInt(params.params.page, 10);
        }
        this.params = params;
        this.render(params.params);
    },

    render:function (params) {
        var news = this.model.models;
        var len = news.length;

        var table = $('<table class="table table-bordered table-stripped"><thead><tr><th>Jornal</th><th>Data</th><th>Mat&eacute;ria</th><th>Palavra</th><th>Jornal</th><th>Data</th><th>Mat&eacute;ria</th></tr></thead><tbody class="news_list"></tbody></table>');
        $(this.el).append(table);

        // get Excel export link
        var exportLink = createExcelExportLink(params.journal1, params.date, params.journal2);
        $(this.el).append("<a href='"+exportLink+"'><img src='images/CSVImportExport.gif' /></a>");

        for (var i = 0; i < len; i++) {
            $('.news_list', this.el).append(new NewsItemView({model: news[i]}).render().el);
        }
        $(this.el).append(new Paginator({model: this.model, page: this.page, newsCount: this.newsCount, params: this.params.params}).render().el);

        return this;
    }

});

var createExcelExportLink = function(journal1, date, journal2) {
    var exportLink = '/news/export';
    var filters = [];
    if (journal1 && journal1.length > 0) {
        filters.push('journal1=' + journal1);
    }
    if (journal2 && journal2.length > 0) {
        filters.push('journal2=' + journal2);
    }
    if (date && date.length > 0) {
        filters.push('date=' + date);
    }
    if (filters.length > 0) {
        for (var i = 0; i < filters.length ; i++) {
            exportLink = exportLink + ((i === 0) ? '?' : '&')  + filters[i];
        }
    }
    return exportLink;
};

window.NewsItemView = Backbone.View.extend({
    tagName: "tr",
    className: 'news',
    initialize: function () {
        this.model.bind("change", this.render, this);
        this.model.bind("destroy", this.close, this);
    },
    render: function () {
        //console.log(this.model.toJSON());
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});
