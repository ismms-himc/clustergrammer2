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
console.log(clustergrammer_gl_1.default);
const d3 = __importStar(require("d3"));
// console.log(d3)
console.log('**********************************************');
console.log('** clustergrammer2 frontend version 0.2.12 **');
console.log('**********************************************');
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign({}, super.defaults(), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'Latest Hello World!!!!!!!!!!', network: '' });
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
    var inst_container = document.getElementById(args.container_name);
    // console.log('inst_container_2', inst_container)
    args.container = inst_container;
    var cgm = clustergrammer_gl_1.default(args);
    // console.log('making clustergram in make_viz');
    // necessary to suppress typescript error
    console.log(cgm);
}
// console.log(make_viz);
class ExampleView extends base_1.DOMWidgetView {
    render() {
        this.value_changed();
        // this.model.on('change:value', this.value_changed, this);
        // console.log('NETWORK: ' + this.model.get('network'))
        var inst_network_string = this.model.get('network');
        var inst_network = JSON.parse(inst_network_string);
        // console.log(inst_network)
        var container_name = this.cid;
        // the cid appears to be the container id, which gives a unique view number
        console.log('container_name', container_name);
        // widget-subarea appears to be limited to a width of ~960px in nbviewer
        var inst_container = d3.select(this.el)
            .append('div')
            .classed('clustergrammer_glidget', true)
            .attr('id', container_name)
            .style('width', '900px')
            .style('height', '1035px')
            .style('border', '2px solid #eee');
        var container_id = '#' + container_name;
        console.log(container_name, inst_container, container_id);
        var heatmap_width = 900;
        // define arguments object
        var args = {
            'container_name': container_name,
            'network': inst_network,
            'viz_width': heatmap_width,
            'viz_height': heatmap_width
        };
        console.log(args);
        setTimeout(make_viz, 10, args);
    }
    value_changed() {
        // this.el.textContent = this.model.get('value');
        console.log('CHANGED');
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map