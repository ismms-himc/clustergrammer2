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

console.log('*********************************************')
console.log('** clustergrammer2 frontend version 0.6.0 **')
console.log('*********************************************')

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
      custom_cat: '{"col":"JS", "row":"JS"}',
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

function make_viz(args, cgm_model){
  args.container = document.getElementById(args.container_name);
  cgm_fun(args, cgm_model);

  // // exposing all of cgm, eventually want to only expose a few methods
  // // cgm_model.cgm = cgm;
  // cgm_model.destroy_viz = cgm.destroy_viz;

}

var my_widget_callback = function(external_model){

  console.log('my_widget_callback!!!!!!!!!!!!!!!!!!!1')

  var cgm = external_model.cgm;
  var params = cgm.params;
  var inst_value;

  console.log(params.tooltip.tooltip_type)

  if (params.tooltip.tooltip_type === 'row-label'){

    // update row/column
    ////////////////////////
    inst_value = params.tooltip.tooltip_type + ' -> ' +
                 String(params.int.mouseover.row.name)

    external_model.model.set('value', inst_value);
    external_model.touch();

  } else if (params.tooltip.tooltip_type === 'col-cat-0'){

    // update second category
    ////////////////////////
    // params.int.mouseover[inst_axis].cats[mouseover_cat_index]
    inst_value = params.tooltip.tooltip_type + ' -> ' +
                 String(params.int.mouseover['col'].cats[0])

    external_model.model.set('value', inst_value);
    external_model.touch();

  } else if (params.tooltip.tooltip_type === 'col-cat-1'){

    // update first category
    ////////////////////////
    // params.int.mouseover[inst_axis].cats[mouseover_cat_index]
    inst_value = params.tooltip.tooltip_type + ' -> ' +
                 String(params.int.mouseover['col'].cats[1])

    external_model.model.set('value', inst_value);
    external_model.touch();

  } else if (params.tooltip.tooltip_type === 'col-dendro') {

      var selected_clust_names = params.dendro.selected_clust_names;
      var tmp_index;
      var real_index;
      var all_labels = new Array();
      var index_list = new Array();

      // Parse titles out of labels (if necessary)
      var ini_all_labels = params.labels.ordered_labels.cols;
      var all_labels = new Array();
      for (let inst_label of ini_all_labels){
        // console.log(inst_label)
        if (inst_label.includes(': ')){
          inst_label = inst_label.split(': ')[1];
        }
        all_labels.push(inst_label);
      }

      // look up indexes in original dataframe
      for (let inst_name of selected_clust_names) {

        // console.log(inst_name)

        // get index of label
        tmp_index = all_labels.indexOf(inst_name)

        // look up index in original dataframe
        real_index = cgm.params.labels.ordered_labels.col_indices[tmp_index]
        index_list.push(real_index);

      }


      var index_list_string = String(index_list)

      inst_value = params.tooltip.tooltip_type + ' -> ' + index_list_string
      external_model.model.set('value', inst_value);
      external_model.touch();

  }
  // else {

  //   console.log('OTHER')

  //   inst_value = params.tooltip.tooltip_type; // 'other'

  //   // update other
  //   ////////////////////////
  //   // external_model.model.set('value', String(null));
  //   external_model.model.set('value', inst_value);
  //   external_model.touch();

  // }

  // let ini_manual_cat_dict = {}
  // if (params.cat_data.manual_cat_dict === '{"col":"", "row":""}'){
  //   ini_manual_cat_dict = true
  // } else {
  //   ini_manual_cat_dict = false
  // }


  if (params.int.manual_update_cats){

    let export_dict = {}

      // transfer manual categories
    if ('col' in params.cat_data.manual_cat_dict){
      export_dict['col'] = params.cat_data.manual_cat_dict.col
      export_dict['col_cat_colors'] = params.cat_colors.col['cat-0']
    }

    if ('row' in params.cat_data.manual_cat_dict){
      export_dict['row'] = params.cat_data.manual_cat_dict.row
      export_dict['row_cat_colors'] = params.cat_colors.row['cat-0']
    }


    // Object.keys(cgm.params.cat_colors.col['cat-0'])

    // let axes = ['row', 'col']
    // let cat_colors = {}
    // let ini_cat_colors = {}
    // let ini_cats


    // if (axis in params.cat_colors){
    //   ini_cat_colors[axis] = params.cat_colors[axis]['cat-0']
    // }

    // ini_cats = Object.keys(ini_cat_colors)

    // ini_cats.forEach(x => {
    //   cat_colors[x.split(': ')[1]] = ini_cat_colors[x]
    // })

    // // cleaned
    // console.log('cleaned cat colors')
    // console.log(cat_colors)

    console.log('>>>>>>>>>>>>>>> manual_update_cats!!!!!!')
    let json_string = JSON.stringify(export_dict)
    external_model.model.set('custom_cat', json_string);
    external_model.touch();
  }
}

export
class ExampleView extends DOMWidgetView {
  render() {

    d3.select(this.el)
      .append('div')
      .attr('id', this.cid)
      .style('width', '900px')
      .style('height', '1035px')
      // .style('border', '2px solid #eee')

    // define arguments object
    var args = {
        'container_name': this.cid,
        'network': JSON.parse(this.model.get('network')),
        'viz_width' : 900,
        'viz_height': 900,
        // 'widget_model': this,
        'widget_callback': my_widget_callback
    };

    setTimeout(make_viz, 10, args, this);

    this.model.on('change:value', this.value_changed, this);

  }

  value_changed() {

    // this can be used to update cgm on a value change to the widget_model
    // e.g. reorder cgm based on value change to widget traitlet

    // console.log('widget_model.value_changed')
    // console.log('--------------------------')
    // console.log(this)

    // console.log('value', this.model.get('value'));

    // // Actually delete the widget and replace with text (not deleting widget state)
    // this.el.textContent = this.model.get('value');

    // // see https://stackoverflow.com/questions/55834241/ts2339-property-name-does-not-exist-on-type-object
    // console.log(this['cgm'])
    // this['cgm'].destroy_viz()

    if (this.model.get('value') === 'destroy-viz'){
      console.log('destroy the viz')
      this['cgm'].destroy_viz();
    }

  }

}



