var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var d3 = require('d3')
var new_module = require('./new_module');
// var $ = require('jquery-ui')
var cgm_fun = require('clustergrammer');

// var gene_info = require('./gene_info');
var hzome = require('./hzome_functions');

var Enrichr_request = require('./enrichr_functions');

require('!style!css!./custom.css');

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
    viz_title : 'default value',
    network: ''
  })
});


// Custom View. Renders the widget model.
var hello_view = widgets.DOMWidgetView.extend({
  render: render_function,

  value_changed: function() {

    this.el.textContent = this.model.get('viz_title');

    var inst_network_string = this.model.get('network');

    inst_network = JSON.parse(inst_network_string);

    d3.select(this.el)
      .classed('.widget_viz',true);

  }
});

function render_function() {

    // var container_name = this.model.get('viz_title');

    var viz_number = d3.selectAll('.clustergrammer_widget')[0].length;

    var container_name = 'cgm_notebook_' + String(viz_number+ 1) ;

    if (d3.selectAll('#'+container_name).empty() == false){
      container_name = container_name + '_alt';
    }

    d3.select(this.el)
        .append('div')
        .classed('clustergrammer_widget', true)
        .attr('id', container_name)
        .style('width', '1000px')
        .style('height', '800px');

    var inst_network_string = this.model.get('network');

    inst_network = JSON.parse(inst_network_string);

    // var about_string = "<img src='clustergrammer_logo.png' style='width:100px'>";
    var about_string = 'Clustergrammer!!!'

    var container_id = '#'+container_name;
    // define arguments object
    var args = {
        root: container_id,
        'network_data': inst_network,
        'about':about_string,
        // 'row_tip_callback':gene_info
        'row_tip_callback':hzome.gene_info,
        'matrix_update_callback':matrix_update_callback,
    };

    setTimeout(make_viz, 10, args);

  }

function make_viz(args){
    var cgm = cgm_fun(args);

    check_setup_enrichr(cgm);

}

// Enrichrgram specific functions
///////////////////////////////////////////////////////////////

function matrix_update_callback(){
  if (genes_were_found){
    enr_obj.clear_enrichr_results();
  }
}

var genes_were_found = false;
function check_setup_enrichr(inst_cgm){

  var all_rows = inst_cgm.params.network_data.row_nodes_names;
  var max_num_genes = 20;

  if (all_rows.length > 20){
    all_rows = all_rows.slice(0,20);
  }

  var wait_unit = 500;
  var wait_time = 0;
  // check each gene using Harmonizome
  _.each(all_rows, function(inst_name){

    // check_gene_request(inst_cgm, inst_name, run_ini_enrichr);
    setTimeout(check_gene_request, wait_time, inst_cgm, inst_name, run_ini_enrichr);

    wait_time = wait_time + wait_unit;

  });

}

function run_ini_enrichr(inst_cgm, inst_name){

  if (genes_were_found){

    if (d3.select('.enrichr_logo').empty()){

      // set up Enrichr category import
      enr_obj = Enrichr_request(inst_cgm);
      enr_obj.enrichr_icon();

      // set up Enrichr export in dendro modal
      //////////////////////////////////////////

      // only display for rows
      var enrichr_section = d3.selectAll('.dendro_info')
        .select('.modal-body')
        .append('div')
        .classed('enrichr_export_section', true)
        .style('margin-top', '10px')
        .style('display','none');

      enrichr_section
        .append('text')
        .text('Send genes to ');

      enrichr_section
        .append('a')
        .html('Enrichr')
        .on('click', function(){

          var group_string = d3.select('.dendro_text input').attr('value');

          // replace all instances of commas with new line
          var gene_list = group_string.replace(/, /g, '\n');

          var enrichr_info = {list: gene_list, description: 'Clustergrammer gene-cluster list' , popup: true};

          // defined globally - will improve
          enrich(enrichr_info);

        });

    }

  }

}

function check_gene_request(inst_cgm, gene_symbol, check_enrichr_callback){

  var base_url = 'https://amp.pharm.mssm.edu/Harmonizome/api/1.0/gene/';
  var url = base_url + gene_symbol;

  if (genes_were_found === false){

    $.get(url, function(data) {

      data = JSON.parse(data);

      if (data.name != undefined){
        genes_were_found = true;
      }

      check_enrichr_callback(inst_cgm, gene_symbol);

    });
  }

}

module.exports = {
  hello_model : hello_model,
  hello_view : hello_view
};
