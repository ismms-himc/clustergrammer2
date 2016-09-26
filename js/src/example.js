var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var d3 = require('d3')
var new_module = require('./new_module');
// var $ = require('jquery-ui')
var cgm_fun = require('clustergrammer');

var gene_info = require('./gene_info');
var Enrichr_request = require('./enrichr_functions');

console.log(gene_info)
console.log(Enrichr_request)

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
  render: render_function,

  value_changed: function() {

    this.el.textContent = this.model.get('value');

    var inst_network_string = this.model.get('network');

    inst_network = JSON.parse(inst_network_string);

    d3.select(this.el)
      .classed('.widget_viz',true);

  }
});

function render_function() {

    var container_name = this.model.get('value');

    d3.select(this.el)
        .append('div')
        .attr('id', container_name)
        .style('width', '1000px')
        .style('height', '800px');

    var inst_network_string = this.model.get('network');
    inst_network = JSON.parse(inst_network_string);

    var container_id = '#'+container_name;
    // define arguments object
    var args = {
        root: container_id,
        'network_data': inst_network,
        'about':'Clustergrammer!',
        'row_tip_callback':gene_info
    };

    setTimeout(make_viz, 10, args);

  }

function make_viz(args){
    var cgm = cgm_fun(args);

    // Enrichr categories
    //////////////////////
    enr_obj = Enrichr_request(cgm);
    enr_obj.enrichr_icon();
}

module.exports = {
  hello_model : hello_model,
  hello_view : hello_view
};
