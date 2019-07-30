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
function make_viz(args, cgm_model) {
    args.container = document.getElementById(args.container_name);
    var cgm = clustergrammer_gl_1.default(args);
    console.log(cgm);
    console.log(cgm_model);
    // // exposing all of cgm, eventually want to only expose a few methods
    // cgm_model.cgm = cgm;
}
var my_widget_callback = function (cgm) {
    var params = cgm.params;
    if (params.tooltip.tooltip_type === 'row-label') {
        params.widget_model.model.set('value', String(params.int.mouseover.row.name));
        params.widget_model.touch();
    }
    else {
        params.widget_model.model.set('value', String(null));
        params.widget_model.touch();
    }
};
class ExampleView extends base_1.DOMWidgetView {
    render() {
        d3.select(this.el)
            .append('div')
            .attr('id', this.cid)
            .style('width', '900px')
            .style('height', '1035px')
            .style('border', '2px solid #eee');
        // define arguments object
        var args = {
            'container_name': this.cid,
            'network': JSON.parse(this.model.get('network')),
            'viz_width': 900,
            'viz_height': 900,
            'widget_model': this,
            'widget_callback': my_widget_callback
        };
        setTimeout(make_viz, 10, args, this);
        this.model.on('change:value', this.value_changed, this);
    }
    value_changed() {
        console.log(this);
        // this.el.textContent = this.model.get('value');
        console.log('checking value!!', this.model.get('value'));
        // // see https://stackoverflow.com/questions/55834241/ts2339-property-name-does-not-exist-on-type-object
        // console.log(this['cgm'])
        // this['cgm'].destroy_viz()
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map