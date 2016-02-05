window.News = Backbone.Model.extend({

    urlRoot: "/news",

    idAttribute: "_id",

    initialize: function () {
        this.attributes.dateFormatted1 = moment(this.attributes.date1, 'YYYY-MM-DD hh:mm:ss').format('DD/MM/YYYY');
        this.attributes.dateFormatted2 = moment(this.attributes.date2, 'YYYY-MM-DD hh:mm:ss').format('DD/MM/YYYY');
        this.validators = {};

        /*this.validators.url = function (value) {
            return value.length > 0 ? {isValid: true} : {isValid: false, message: "You must enter a URL"};
        };*/
    },

    validateItem: function (key) {
        return (this.validators[key]) ? this.validators[key](this.get(key)) : {isValid: true};
    },

    // TODO: Implement Backbone's standard validate() method instead.
    validateAll: function () {

        var messages = {};

        for (var key in this.validators) {
            if(this.validators.hasOwnProperty(key)) {
                var check = this.validators[key](this.get(key));
                if (check.isValid === false) {
                    messages[key] = check.message;
                }
            }
        }

        return _.size(messages) > 0 ? {isValid: false, messages: messages} : {isValid: true};
    },

    defaults: {
        _id: null,
        url1: "",
        journal1: "",
        date1: "",
        dateFormatted1: "",
        title1: "",
        token: "",
        url2: "",
        journal2: "",
        date2: "",
        dateFormatted2: "",
        title2: "",
    }
});

window.NewsCollection = Backbone.Collection.extend({

    model: News,

    url: "/news"

});

window.NewsCounter = Backbone.Model.extend({
    urlRoot: "/news/count",

    initialize: function () {

    },

    defaults: {
        total: 0
    }
});

// Stats 1
window.Stats1 = Backbone.Model.extend({

    initialize: function() {

    },

    defaults: {
        journal: "",
        total: 0
    }

});

window.Stats1List = Backbone.Collection.extend({

    model: Stats1,

    url: "/stats/1"

});

// Stats 2
window.Stats2 = Backbone.Model.extend({

    urlRoot: "/stats/2",

    initialize: function() {

    },

    defaults: {
        total: 0
    }

});

// Stats 3
window.Stats3 = Backbone.Model.extend({

    initialize: function() {

    },

    defaults: {
        journal: "",
        total: 0
    }

});

window.Stats3List = Backbone.Collection.extend({

    model: Stats3,

    url: "/stats/3"

});

// Stats 4
window.Stats4 = Backbone.Model.extend({

    initialize: function() {

    },

    defaults: {
        journal1: "",
        total: 0,
        journal2: ""
    }

});

window.Stats4List = Backbone.Collection.extend({

    model: Stats4,

    url: "/stats/4"

});

// Stats 5
window.Stats5 = Backbone.Model.extend({

    initialize: function() {

    },

    defaults: {
        date: "",
        journal: "",
        total: 0
    }

});

window.Stats5List = Backbone.Collection.extend({

    model: Stats5,

    url: "/stats/5"

});
