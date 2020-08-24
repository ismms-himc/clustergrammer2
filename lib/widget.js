"use strict";
// Copyright (c) Nicolas Fernandez.
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const base_1 = require("@jupyter-widgets/base");
const version_1 = require("./version");
const clustergrammer_gl_1 = __importDefault(require("clustergrammer-gl"));
const d3 = __importStar(require("d3"));
console.log('*********************************************');
console.log('** clustergrammer2 frontend version 0.17.0 **');
console.log('*********************************************');
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign({}, super.defaults(), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'javascript set value!!!', manual_cat: '{"col":"JS", "row":"JS"}', network: '' });
    }
}
ExampleModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ExampleModel.model_name = 'ExampleModel';
ExampleModel.model_module = version_1.MODULE_NAME;
ExampleModel.model_module_version = version_1.MODULE_VERSION;
ExampleModel.view_name = 'ExampleView'; // Set to null if no view
ExampleModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ExampleModel.view_module_version = version_1.MODULE_VERSION;
exports.ExampleModel = ExampleModel;
function make_viz(args, cgm_model) {
    args.container = document.getElementById(args.container_name);
    clustergrammer_gl_1.default(args, cgm_model);
    // // exposing all of cgm, eventually want to only expose a few methods
    // // cgm_model.cgm = cgm;
    // cgm_model.destroy_viz = cgm.destroy_viz;
}
var my_widget_callback = function (external_model) {
    console.log('my_widget_callback!!!!!!!!!!!!!!!!!!!1');
    var cgm = external_model.cgm;
    var params = cgm.params;
    var inst_value;
    console.log(params.tooltip.tooltip_type);
    if (params.tooltip.tooltip_type === 'row-label') {
        // update row/column
        ////////////////////////
        inst_value = params.tooltip.tooltip_type + ' -> ' +
            String(params.int.mouseover.row.name);
        external_model.model.set('value', inst_value);
        external_model.touch();
    }
    else if (params.tooltip.tooltip_type === 'col-cat-0') {
        // update second category
        ////////////////////////
        // params.int.mouseover[inst_axis].cats[mouseover_cat_index]
        inst_value = params.tooltip.tooltip_type + ' -> ' +
            String(params.int.mouseover['col'].cats[0]);
        external_model.model.set('value', inst_value);
        external_model.touch();
    }
    else if (params.tooltip.tooltip_type === 'col-cat-1') {
        // update first category
        ////////////////////////
        // params.int.mouseover[inst_axis].cats[mouseover_cat_index]
        inst_value = params.tooltip.tooltip_type + ' -> ' +
            String(params.int.mouseover['col'].cats[1]);
        external_model.model.set('value', inst_value);
        external_model.touch();
    }
    else if (params.tooltip.tooltip_type === 'col-dendro') {
        var selected_clust_names = params.dendro.selected_clust_names;
        var tmp_index;
        var real_index;
        var all_labels = new Array();
        var index_list = new Array();
        // Parse titles out of labels (if necessary)
        var ini_all_labels = params.labels.ordered_labels.cols;
        var all_labels = new Array();
        for (let inst_label of ini_all_labels) {
            // console.log(inst_label)
            if (inst_label.includes(': ')) {
                inst_label = inst_label.split(': ')[1];
            }
            all_labels.push(inst_label);
        }
        // look up indexes in original dataframe
        for (let inst_name of selected_clust_names) {
            // get index of label
            tmp_index = all_labels.indexOf(inst_name);
            // look up index in original dataframe
            real_index = cgm.params.labels.ordered_labels.col_indices[tmp_index];
            index_list.push(real_index);
        }
        var index_list_string = String(index_list);
        console.log('interaciting!!!!!!!!!s');
        inst_value = params.tooltip.tooltip_type + ' -> ' + index_list_string;
        external_model.model.set('value', inst_value);
        external_model.touch();
    }
    if (params.int.manual_update_cats) {
        let export_dict = {};
        // transfer manual categories
        if ('col' in params.cat_data.manual_cat_dict) {
            export_dict['col'] = params.cat_data.manual_cat_dict.col;
            // export_dict['col_cat_colors'] = params.cat_colors.col['cat-0']
        }
        if ('row' in params.cat_data.manual_cat_dict) {
            export_dict['row'] = params.cat_data.manual_cat_dict.row;
            // export_dict['row_cat_colors'] = params.cat_colors.row['cat-0']
        }
        export_dict['global_cat_colors'] = params.viz.global_cat_colors;
        let json_string = JSON.stringify(export_dict);
        external_model.model.set('manual_cat', json_string);
        external_model.touch();
        // notify manual_cat_update that update is not necessary
        params.self_update = true;
        console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>');
        console.log('setting self_update to true');
        console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>');
    }
};
class ExampleView extends base_1.DOMWidgetView {
    render() {
        d3.select(this.el)
            .append('div')
            .attr('id', this.cid)
            .style('width', '900px')
            .style('height', '1035px');
        // .style('border', '2px solid #eee')
        // define arguments object
        var args = {
            'container_name': this.cid,
            'network': JSON.parse(this.model.get('network')),
            'viz_width': 900,
            'viz_height': 900,
            // 'widget_model': this,
            'widget_callback': my_widget_callback
        };
        setTimeout(make_viz, 10, args, this);
        this.model.on('change:value', this.value_changed, this);
        this.model.on('change:manual_cat', this.manual_cat_update, this);
    }
    value_changed() {
        console.log('value changed!!!!!!!!!!!!');
        if (this.model.get('value') === 'destroy-viz') {
            console.log('destroy the viz');
            this['cgm'].destroy_viz();
        }
    }
    manual_cat_update() {
        console.log('***********************************************');
        console.log('* manual update to cat from backend');
        console.log('***********************************************');
        let dict_manual_cat = JSON.parse(this.model.get('manual_cat'));
        // console.log(dict_manual_cat)
        // console.log('getting col from manual_cat')
        // console.log(dict_manual_cat['col'])
        let manual_category_name = this['cgm']['params']['network']['manual_category']['col'];
        let update_cat_dict = dict_manual_cat['col'][manual_category_name];
        // we don't want to have undefined categories
        // console.log('for each coming up!')
        let new_cat_dict = {};
        this['cgm']['params']['network']['col_nodes']
            .forEach(x => {
            // assuming no title in name
            let inst_name = x['name'];
            let orig_cat = x['cat-0'].split(': ')[1];
            // console.log(inst_name, orig_cat)
            if (inst_name in update_cat_dict) {
                new_cat_dict[inst_name] = update_cat_dict[inst_name];
            }
            else {
                new_cat_dict[inst_name] = orig_cat;
            }
        });
        // console.log('**********************************************')
        // console.log('**********************************************')
        // console.log('**********************************************')
        // console.log('**********************************************')
        // console.log(new_cat_dict)
        this['cgm']['update_all_cats'](this['cgm'], 'col', manual_category_name, new_cat_dict);
        // console.log(this['cgm']);
        // let axis = 'col';
        // let cat_title = this['cgm'].params.network.manual_category.col;
        // this['cgm'].params.network[axis + '_nodes']
        //     .map(x => {
        //        let new_cat = this['cgm'].params.cat_data.manual_cat_dict[axis];
        //        let full_cat = cat_title + ': ' + new_cat;
        //        let inst_name = x.name;
        //        if ( inst_name.includes(': ') ){
        //          inst_name = inst_name.split(': ')[1]
        //        }
        //        x['cat-0'] = full_cat
        //      })
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map