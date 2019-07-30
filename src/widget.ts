// Copyright (c) Nicolas Fernandez.
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import cgm_fun from 'clustergrammer-gl';

import * as d3 from 'd3';

console.log('********************************************')
console.log('** clustergrammer2 frontend version 0.4.3 **')
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

function make_dom(inst_element, container_name){
  d3.select(inst_element)
    .append('div')
    .attr('id', container_name)
    .style('width', '900px')
    .style('height', '1035px')
    .style('border', '2px solid #eee');
}

function make_viz(args){

  var inst_container = document.getElementById(args.container_name)
  args.container = inst_container;
  cgm_fun(args);

}

export
class ExampleView extends DOMWidgetView {
  render() {

    var inst_network = JSON.parse(this.model.get('network'));
    var container_name = this.cid;

    // the cid appears to be the container id, which gives a unique view number
    console.log('container_name', container_name)

    var my_widget_callback = function(cgm){

      var params = cgm.params;
      if (params.tooltip.tooltip_type === 'row-label'){
        params.widget_model.model.set('value', String(params.int.mouseover.row.name));
        params.widget_model.touch();
      } else {
        params.widget_model.model.set('value', String(null));
        params.widget_model.touch();
      }
    }

    // define arguments object
    var args = {
        'container_name': container_name,
        'network': inst_network,
        'viz_width' : 900,
        'viz_height': 900,
        'widget_model': this,
        'widget_callback': my_widget_callback
    };

    make_dom(this.el, container_name);
    setTimeout(make_viz, 10, args);

    this.model.on('change:value', this.value_changed, this);
    this.model.on('change:mat_string', this.update_mat_string, this);

  }

  value_changed() {
    // this.el.textContent = this.model.get('value');
    console.log('checking value', this.model.get('value'))

  }
  update_mat_string(){
    console.log('checking mat_string', this.model.get('mat_string'))
  }
}



