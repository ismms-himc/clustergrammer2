// Copyright (c) Nicolas Fernandez.
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import cgm_fun from 'clustergrammer-gl';
console.log(cgm_fun);

import * as d3 from 'd3';
// console.log(d3)

console.log('********************************************')
console.log('** clustergrammer2 frontend version 0.3.0 **')
console.log('********************************************')

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
      value : 'Latest Hello World!!!!!!!!!!',
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
  var inst_container = document.getElementById(args.container_name)
  // console.log('inst_container_2', inst_container)
  args.container = inst_container;
  var cgm = cgm_fun(args)
  // console.log('making clustergram in make_viz');

  // necessary to suppress typescript error
  console.log(cgm);
}

// console.log(make_viz);

export
class ExampleView extends DOMWidgetView {
  render() {
    this.value_changed();
    // this.model.on('change:value', this.value_changed, this);
    // console.log('NETWORK: ' + this.model.get('network'))

    var inst_network_string = this.model.get('network');

    var inst_network = JSON.parse(inst_network_string);

    // console.log(inst_network)

    var container_name = this.cid;

    // the cid appears to be the container id, which gives a unique view number
    console.log('container_name', container_name)

    // widget-subarea appears to be limited to a width of ~960px in nbviewer
    var inst_container = d3.select(this.el)
        .append('div')
        .classed('clustergrammer_glidget', true)
        .attr('id', container_name)
        .style('width', '900px')
        .style('height', '1035px')
        .style('border', '2px solid #eee');

    var container_id = '#'+container_name;

    console.log(container_name, inst_container, container_id);

    var heatmap_width = 900;

    // define arguments object
    var args = {
        'container_name': container_name,
        'network': inst_network,
        'viz_width' : heatmap_width,
        'viz_height': heatmap_width
    };

    console.log(args);

    // may want to save output in order to clear out old widgets:
    setTimeout(make_viz, 10, args);
  }

  value_changed() {
    // this.el.textContent = this.model.get('value');
    console.log('CHANGED')
  }
}


