"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const base_1 = require("@jupyter-widgets/base");
const widgetExports = __importStar(require("./widget"));
const version_1 = require("./version");
const EXTENSION_ID = 'jupyter.extensions.clustergrammer2';
/**
 * The example plugin.
 */
const examplePlugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
};
exports.default = examplePlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: version_1.MODULE_NAME,
        version: version_1.MODULE_VERSION,
        exports: widgetExports,
    });
}
//# sourceMappingURL=plugin.js.map