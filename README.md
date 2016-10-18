clustergrammer_widget
===============================

clustergrammer_widget

Installation
------------

To install use pip:

    $ pip install clustergrammer_widget
    $ jupyter nbextension enable --py --sys-prefix clustergrammer_widget


For a development installation (requires npm),

    $ git clone https://github.com/maayanlab/clustergrammer-widget.git
    $ cd clustergrammer-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --user clustergrammer-widget
    $ jupyter nbextension enable --py --user clustergrammer-widget
