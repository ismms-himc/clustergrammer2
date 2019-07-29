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
// console.log(cgm_fun);
const d3 = __importStar(require("d3"));
// console.log(d3)
console.log('********************************************');
console.log('** clustergrammer2 frontend version 0.4.3 **');
console.log('********************************************');
console.log('working on traitlets for Voila');
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign({}, super.defaults(), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'javascript set value!!!', network: '' });
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
function make_viz(args) {
    console.log('3: make_viz');
    console.log('need to check whether container is empty');
    console.log('is empty: ', d3.select('#' + args.container_name).empty());
    var inst_container = document.getElementById(args.container_name);
    args.container = inst_container;
    var cgm = clustergrammer_gl_1.default(args);
    d3.select(cgm.params.root).on('mouseover', function () {
        console.log('updating stuff and running touch');
        args.widget_model.model.set('value', String(cgm.params.int.mouseover.row.name));
        args.widget_model.model.set('mat_string', 'click-mat-string');
        args.widget_model.touch();
    });
    // console.log(cgm);
}
// console.log(make_viz);
class ExampleView extends base_1.DOMWidgetView {
    render() {
        // this.value_changed();
        this.model.on('change:value', this.value_changed, this);
        this.model.on('change:mat_string', this.update_mat_string, this);
        var inst_network = JSON.parse(this.model.get('network'));
        var container_name = this.cid;
        // the cid appears to be the container id, which gives a unique view number
        console.log('container_name', container_name);
        var cgm_model = this;
        console.log(cgm_model);
        var my_widget_callback = function (cgm) {
            console.log('RUNNING MY WIDGET CALLBACK -- widget model search 2!');
            console.log('defining some widget in index.html');
            console.log(cgm.params.widget_model);
            console.log('tooltip type');
            console.log(cgm.params.tooltip.tooltip_type);
            if (cgm.params.tooltip.tooltip_type === 'row-label') {
                cgm.params.widget_model.model.set('value', String(cgm.params.int.mouseover.row.name));
                cgm.params.widget_model.touch();
            }
        };
        // define arguments object
        var args = {
            'container_name': container_name,
            'network': inst_network,
            'viz_width': 900,
            'viz_height': 900,
            'widget_model': cgm_model,
            'widget_callback': my_widget_callback
        };
        function make_dom(inst_element, container_name) {
            console.log('1: D3 append div');
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
        console.log('checking value', this.model.get('value'));
    }
    update_mat_string() {
        console.log('checking mat_string', this.model.get('mat_string'));
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map