# Clustergrammer2 Roadmap

Clustergrammer2 is a Jupyter Widget that enables researchers to interactively explore and analyze high-dimensional single-cell data. Our immediate goals are to improve the interactive visualization as well as add additional data analysis methods. 

If you have feedback or concerns please submit an issue on GitHub.

Last updated: July 9, 2019

## Interactive Visualization High-Dimensional Single Cell Data
Clustergrammer2 allows users to interactively explore single-cell datasets consisting of millions of data points. We are continuing to improve the interactive visualization user experience (e.g. add functionaltiy). 

Clustergrammer2 uses the JavaScript library [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl) to generate the interactive heatmaps. Clustergrammer-GL is built using the WebGL library [regl](https://github.com/regl-project/regl). Development of the interactive WebGL visualizations are primarily done on the [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl) repo. 

## Single-Cell Data Analysis
We are working on additing additional data analysis methods to facilitate exploration and analysis of single cell data. The Python back-end of Clustergrammer2 handles data analysis tasks (e.g. filtering, normalization, clustering) and development of additional data analysis methods is done in this repo. 

## Building Dashboards
We are working on using the librray [voila](https://github.com/QuantStack/voila) for generating dashboards. The [Jupyter Widgets](https://github.com/jupyter-widgets) framework enables communication between widgets and we are currently working on using this feature to build dashboards using Clustergrammer2.

## Examples
We are currently working on examples Jupyter notebooks using Clustergrammer2. Users can run these example noteooks by installing Clustergrammer2 locally or for free using several cloud-based Jupyter instances: 
* MyBinder
* Kaggle
* Saturn Cloud

## Documentation 
The broader Clustergrammer project spans several inter-connected projects: 
* [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl)
* [Clustergrammer-JS](https://github.com/maayanlab/clustergrammer)
* [Clustergrammer-PY](https://github.com/maayanlab/clustergrammer-py)
* [Clustergrammer-Widget](https://github.com/maayanlab/clustergrammer-widget)
* [Clustergrammer-Web](https://github.com/maayanlab/clustergrammer-web)

Documentation can be found here [clustergrammer.readthedocs.io/](https://clustergrammer.readthedocs.io/). We will be improving documentation for Clustergrammer2.

## Implement Testing and Continuous Integration
Please see [issue #30](https://github.com/ismms-himc/clustergrammer2/issues/30).
