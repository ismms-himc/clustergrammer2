define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                'clustergrammer2': 'nbextensions/clustergrammer2/index',
            },
        }
    });
    // Export the required load_ipython_extention
    return {
        load_ipython_extension : function() {}
    };
});
