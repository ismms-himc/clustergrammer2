# Clustergrammer2 Roadmap

Clustergrammer2 is a Jupyter Widget that enables researchers to interactively explore and analyze high-dimensional single-cell data. Our goals are to:

* improve the interactive visualization
* add and improve additional data analysis methods (e.g. gene signature methods)

If you have feedback or concerns please submit an issue on GitHub.

Last updated: July 9, 2019

# Interactive Visualization High-Dimensional Single Cell Data
Clustergrammer2 allows users to interactively explore single-cell datasets consisting of millions of data points (e.g. thousands of single cells in thousands of dimensions). Clustergrammer2 uses the JavaScript library [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl) to generate the interactive heatmaps. Clustergrammer-GL is built using the WebGL library [regl](https://github.com/regl-project/regl). Development of the interactive WebGL visualizations are primarily done on the [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl) repo.

# Single-Cell Data Analysis
We are working on additing additional data analysis methods to facilitate exploration and analysis of single cell data. The Python back-end of Clustergrammer2 handles data analysis tasks (e.g. filtering, normalization, clustering) and development of additional data analysis methods is done in this repo. We are also working on integration of location-based data (e.g. multiplex ion-beam imaging, CODEX) into Clustergrammer's workflows.

# Building Dashboards
We are working on using the librray [voila](https://github.com/QuantStack/voila) for generating dashboards. The [Jupyter Widgets](https://github.com/jupyter-widgets) framework enables communication between widgets and we are currently working on using this feature to build dashboards using Clustergrammer2.

# Examples
We are currently working on examples Jupyter notebooks using Clustergrammer2 (see [Clustergrammer2-Notebooks](https://github.com/ismms-himc/clustergrammer2-notebooks) and [Cast Studies and Tutorials](https://clustergrammer.readthedocs.io/case_studies.html)). Users can run these example noteooks by installing Clustergrammer2 locally or for free using several cloud-based Jupyter instances:
* MyBinder
* Saturn Cloud
* Kaggle

# Issues
## High Priority
* [Jupyter Lab 1.0 Bug](https://github.com/ismms-himc/clustergrammer2/issues/48)
* [Improve API](https://github.com/ismms-himc/clustergrammer2/issues/34)
* [testing and continuous integration](https://github.com/ismms-himc/clustergrammer2/issues/30)
* [Clear Old WebGL State](https://github.com/ismms-himc/clustergrammer2/issues/5)
* [Dendrogram Slicing](https://github.com/ismms-himc/clustergrammer2/issues/49)
* [Initial Ordering](https://github.com/ismms-himc/clustergrammer2/issues/1)

## Normal Priority
* [Save and Load Pre-clustered Views](https://github.com/ismms-himc/clustergrammer2/issues/40)
* [Zarr read/write](https://github.com/ismms-himc/clustergrammer2/issues/38)
* [Local Enrichment Analysis](https://github.com/ismms-himc/clustergrammer2/issues/10)

# Documentation
The broader Clustergrammer project documentation can be found here [clustergrammer.readthedocs.io/](https://clustergrammer.readthedocs.io/).
