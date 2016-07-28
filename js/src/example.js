var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var d3 = require('d3');
var new_module = require('./new_module');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including `_model_name`, `_view_name`, `_model_module`
// and `_view_module` when different from the base class.
//
// When serialiazing entire widget state for embedding, only values different from the
// defaults will be specified.
var hello_model = widgets.DOMWidgetModel.extend({
  defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
    _view_name : 'hello_view',
    _model_name : 'hello_model',
    _view_module : 'clustergrammer_widget',
    _model_module : 'clustergrammer_widget',
    value : 'default value',
    network: ''
  })
});


// Custom View. Renders the widget model.
var hello_view = widgets.DOMWidgetView.extend({
  render: function() {
    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  },

  value_changed: function() {

    this.el.textContent = this.model.get('value');

    var inst_network_string = this.model.get('network');

    inst_network = JSON.parse(inst_network_string);

    $(this.el).click(
      function(){
        new_module();
        console.log(inst_network);
      })

    d3.select(this.el)
      .classed('widget_viz',true);



  }
});


module.exports = {
  hello_model : hello_model,
  hello_view : hello_view
};
