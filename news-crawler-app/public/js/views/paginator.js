window.Paginator = Backbone.View.extend({

    className: "pagination pagination-centered",

    initialize:function (params) {
        this.model.bind("reset", this.render, this);
        this.page = params.page;
        var filter = '';
        var first = true;
        for (parameter in params.params) {
            if (parameter === "page")
                continue;
            var value = params.params[parameter];
            if (first) {
                filter = filter + parameter + '=' + value;
                first = false;
            }
            else
                filter = filter + '&' + parameter + '=' + value;
        }
        if (filter.length > 0)
            filter = filter + '&';
        this.filter = filter;
        this.newsCount = params.newsCount;
        this.render();
    },

    render:function () {
        var items = this.model.models;
        var pageCount = Math.floor(this.newsCount / 50);

        $(this.el).html('<ul class="pagination" />');

        for (var i=0; i < pageCount; i++) {
            $('ul', this.el).append("<li" + ((i + 1) === this.page ? " class='active'" : "") + "><a href='#news?"+this.filter+"page="+(i+1)+"'>" + (i+1) + "</a></li>");
        }

        return this;
    }
});
