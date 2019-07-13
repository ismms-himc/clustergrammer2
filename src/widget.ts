// Copyright (c) Nicolas Fernandez.
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import cgm_fun from 'clustergrammer-gl';
// console.log(cgm_fun);

import * as d3 from 'd3';
// console.log(d3)

console.log('********************************************')
console.log('** clustergrammer2 frontend version 0.4.2 **')
console.log('********************************************')
console.log('working on traitlets for Voila')

export
class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      value : 'javascript set value!!!',
      network: ''
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

function make_viz(args){
  console.log('3: make_viz')

  console.log('need to check whether container is empty')
  console.log('is empty: ', d3.select('#' + args.container_name).empty())
  var inst_container = document.getElementById(args.container_name)
  args.container = inst_container;

  var cgm = cgm_fun(args)

  d3.select(cgm.params.root).on('mouseover', function(){
    args.widget_model.model.set('value', String(cgm.params.int.mouseover.row.name));
    args.widget_model.model.set('mat_string', 'click-mat-string');
    args.widget_model.touch();
  });

  // console.log(cgm);
}

// console.log(make_viz);

export
class ExampleView extends DOMWidgetView {
  render() {

    // this.value_changed();
    this.model.on('change:value', this.value_changed, this);


    this.model.on('change:mat_string', this.update_mat_string, this);

    var inst_network = JSON.parse(this.model.get('network'));

    var container_name = this.cid;

    // the cid appears to be the container id, which gives a unique view number
    console.log('container_name', container_name)

    var cgm_model = this;
    console.log(cgm_model);

    // define arguments object
    var args = {
        'container_name': container_name,
        'network': inst_network,
        'viz_width' : 900,
        'viz_height': 900,
        'widget_model': cgm_model
    };

    function make_dom(inst_element, container_name){
      console.log('1: D3 append div')
      d3.select(inst_element)
        .append('div')
        .classed('clustergrammer_glidget', true)
        .attr('id', container_name)
        .style('width', '900px')
        .style('height', '1035px')
        .style('border', '2px solid #eee');
    }

    make_dom(this.el, container_name);
    setTimeout(make_viz, 10, args);

    /* Promise version */
    // attempting to wait until DOM is created
    //
    // var make_dom_promise = function(inst_element, container_name) {
    //   return new Promise(function(resolve, reject) {
    //     make_dom(inst_element, container_name)
    //     resolve();
    //   });
    // }

    // make_dom_promise(this.el, container_name).then(
    //   function(){
    //     console.log('finished promise and make_viz')

    //     // may want to save output in order to clear out old widgets
    //     console.log('2: setTimeout')
    //     setTimeout(make_viz, 10, args);
    //     // make_viz(args)
    //   }
    // );

    // widget-subarea appears to be limited to a width of ~960px in nbviewer
    // var inst_container = d3.select(this.el)
    // defining a variable, going to pass this to callback
    // var container_id = '#'+container_name;

    // console.log(container_name);

    // trying to have front-end set value
    // this.model.set('value', 'front-end-set string');
    // d3.select('#' + container_name)
    //   .on('mouseover', function(){
    //     console.log('mouse over widget controlled')
    //   })

  }

  value_changed() {
    // this.el.textContent = this.model.get('value');
    console.log('checking value', this.model.get('value'))
  }

  update_mat_string(){
    console.log('checking mat_string', this.model.get('mat_string'))
  }
}



