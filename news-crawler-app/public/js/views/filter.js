window.FilterView = Backbone.View.extend({

    initialize:function (params) {
        this.render(params);
    },

    render:function (params) {
        $(this.el).html(this.template(params));
        return this;
    }

});
