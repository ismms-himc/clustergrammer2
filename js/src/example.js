var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var d3 = require('d3')
var new_module = require('./new_module');
// var $ = require('jquery-ui')
var cgm_mod = require('./Clustergrammer');

cgm_fun = cgm_mod();


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

    console.log('rendering')

    // // disabling changing behavior
    // this.value_changed();
    // this.model.on('change:value', this.value_changed, this);

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
        'about':'Zoom, scroll, and click buttons to interact with the clustergram.',
    };

    console.log('rendering')
    setTimeout(make_viz, 1000, args);

  },

  value_changed: function() {

    this.el.textContent = this.model.get('value');

    var inst_network_string = this.model.get('network');

    inst_network = JSON.parse(inst_network_string);

    // // define arguments object
    // var args = {
    //     root: '#container-id-1',
    //     'network_data': inst_network,
    //     'about':'Zoom, scroll, and click buttons to interact with the clustergram.',
    // };

    // $(this.el).click(
    //   function(){

    //     new_module();

    //     console.log(inst_network);
    //     console.log(this)

    //     console.log('\n\n\nempty container?')
    //     console.log(d3.select('#container-id-1').empty())

    //     // console.log(cgm_fun)
    //     // var cgm = cgm_fun(args);

    //   })

    d3.select(this.el)
      .classed('.widget_viz',true);

  }
});


function make_viz(args){
    console.log(cgm_fun)
    var cgm = cgm_fun(args);
}

module.exports = {
  hello_model : hello_model,
  hello_view : hello_view
};
