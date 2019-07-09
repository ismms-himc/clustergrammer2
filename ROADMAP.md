# Clustergrammer2 Roadmap

Clustergrammer2 enables researchers to interactively explore and analyze single cell data. Our immediate goals are to improve the interactive visualization as well as add additional data analysis methods. If you have feedback or concerns please submit an issue on GitHub.

Last updated: July 9, 2019

## Interactive Visualization High-Dimensional Single Cell Data
Clustergrammer2 is a Jupyter Widget built using the JavaScript library [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl). Clustergrammer-GL is built using [regl](https://github.com/regl-project/regl) and generates the interactive WebGL heatmap visualization. Development of the interactive WebGL visualization is done on the [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl) repo. 

## Single Cell Data Analysis
The Python back-end of Clustergrammer2 handles data analysis tasks (e.g. filtering, normalization, clustering). 

## Improve Documentation and Examples
The broader Clustergrammer project spans several smaller and inter-connected projects (e.g. [Clustergrammer-JS](https://github.com/maayanlab/clustergrammer), [Clustergrammer-GL](https://github.com/ismms-himc/clustergrammer-gl)) and documentation can be found here [clustergrammer.readthedocs.io/](https://clustergrammer.readthedocs.io/).

## Implement Testing and Continuous Integration
Please see [issue #30](https://github.com/ismms-himc/clustergrammer2/issues/30).
