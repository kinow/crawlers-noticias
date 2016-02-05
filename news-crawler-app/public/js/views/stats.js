window.StatsView = Backbone.View.extend({

  initialize: function() {
    this.render();
  },

  render: function() {
    var div = $("<div class='container-fluid' />");

    var self = this;
    var row1 = $("<div class='row-fluid' />");

    var stats1and2 = $("<div class='col-xs-3' />");
    var stats1 = new Stats1List();
    stats1.fetch({
      success: function() {
        var stats1View = new Stats1View(stats1.models);
        stats1and2.append(stats1View.el);
      }
    });

    var stats2 = new Stats2();
    stats2.fetch({
      success: function() {
        var stats2View = new Stats2View(stats2.attributes.total);
        stats1and2.append(stats2View.el);
      }
    });

    row1.append(stats1and2);

    var stats3 = new Stats3List();
    stats3.fetch({
      success: function() {
        var stats3View = new Stats3View(stats3.models);
        row1.append(stats3View.el);
      }
    });

    var stats4 = new Stats4List();
    stats4.fetch({
      success: function() {
        var stats4View = new Stats4View(stats4.models);
        row1.append(stats4View.el);
      }
    });

    div.append(row1);

    var row2 = $("<div class='row-fluid' />");

    var stats5 = new Stats5List();
    stats5.fetch({
      success: function() {
        stats1.fetch({
          success: function() {
            var journals = stats1.models.map(function(entry) { return (entry.attributes['n1.journal']); });
            var stats5View = new Stats5View(stats5.models, journals);
            row2.append(stats5View.el);
          }
        });
      }
    });

    div.append(row2);

    $(this.el).append(div);

    return this;
  }

});

window.Stats1View = Backbone.View.extend({

  tagName: 'div',

  initialize: function(models) {
    this.models = models;
    this.render();
  },

  render: function() {
    $(this.el).html(this.template({
      list: this.models
    }));
    return this;
  }

});

window.Stats2View = Backbone.View.extend({

  tagName: 'div',

  initialize: function(total) {
    this.total = total;
    this.render();
  },

  render: function() {
    $(this.el).html(this.template({
      total: this.total
    }));
    return this;
  }

});

window.Stats3View = Backbone.View.extend({

  tagName: 'div',

  className: 'col-xs-5',

  initialize: function(models) {
    this.models = models;
    this.render();
  },

  render: function() {
    $(this.el).html(this.template({
      list: this.models
    }));
    return this;
  }

});

window.Stats4View = Backbone.View.extend({

  tagName: 'div',

  className: 'col-xs-4',

  initialize: function(models) {
    this.models = models;
    this.render();
  },

  render: function() {
    $(this.el).html(this.template({
      list: this.models
    }));
    return this;
  }

});

Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
};

function getDates(startDate, stopDate) {
    var dateArray = new Array();
    var currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push( new Date (currentDate) )
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
};

window.Stats5View = Backbone.View.extend({

  tagName: 'div',

  className: 'col-xs-12',

  initialize: function(models, journals) {
    this.journals = journals;
    this.models = models;
    this.render();
  },

  render: function() {
    var dict = {};

    var fromDate = new Date('2014-12-01');
    var toDate = new Date('2015-02-28');

    var dateArray = getDates(fromDate, toDate);
    for (var i = 0; i < dateArray.length; i++) {
      var day = dateArray[i];
      var key = day.toISOString().substring(0, 10) + ' 00:00:00';
      dict[key] = {};
      for (var j = 0; j < this.journals.length; j++) {
        var journal = this.journals[j];
        if (dict[key][journal] === undefined) {
          dict[key][journal] = {};
        }
        dict[key][journal] = {
          date: day,
          journal: journal,
          total: 0
        };
      }
    }

    this.models.map(function (entry) {
      var journal = entry.attributes.journal;
      var date = entry.attributes.date;
      var total = entry.attributes.total;
      dict[date][journal].total = total;
    });
    $(this.el).html(this.template({
      journals: this.journals,
      days: dict
    }));
    return this;
  }

});
