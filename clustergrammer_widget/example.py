import ipywidgets as widgets
import json
from traitlets import Unicode
from clustergrammer import Network

@widgets.register('hello.Hello')
class clustergrammer_notebook(widgets.DOMWidget):
    """"""
    _view_name = Unicode('hello_view').tag(sync=True)
    _model_name = Unicode('hello_model').tag(sync=True)
    _view_module = Unicode('clustergrammer_widget').tag(sync=True)
    _model_module = Unicode('clustergrammer_widget').tag(sync=True)

    viz_title = Unicode('updating python by restarting kernel').tag(sync=True)

    network = Unicode('').tag(sync=True)

