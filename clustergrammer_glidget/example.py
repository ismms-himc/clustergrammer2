import ipywidgets as widgets
import json
from traitlets import Unicode
# from clustergrammer import Network
from . import clustergrammer
Network = clustergrammer.Network

# version 0.3.0

@widgets.register('hello.Hello')
class clustergrammer_glidget(widgets.DOMWidget):
    """
    Clustergrammer-Widget generates an interactive heatmap in the Jupyter
    notebook. Clustergrammer-Widget inherits from Clustergrammer.py which can
    be used to load data, filter, normalize, and cluster.
    """
    _view_name = Unicode('hello_view').tag(sync=True)
    _model_name = Unicode('hello_model').tag(sync=True)
    _view_module = Unicode('clustergrammer_glidget').tag(sync=True)
    _model_module = Unicode('clustergrammer_glidget').tag(sync=True)

    mat_string = Unicode('').tag(sync=True)

    viz_title = Unicode('updating python by restarting kernel').tag(sync=True)

    network = Unicode('').tag(sync=True)
