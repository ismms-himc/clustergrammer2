# Development

During development run `npm run watch` for real time updates. When releasing a new version, first confirm that latest version of the front and back ends are working locally (check console logs, etc).

#### Updating versions
Update the versions in the following files

##### JavaScript

* package.json
* widget.ts

#### Python

* _version.py
* example.py
* requirements.txt
* _frontend.py


#### Webpack

Run the following commands to build the JavaScript bundle:

```bash
npm run build
npm run build:nbextension
npm run build:labextension
```

Publish to npm using
```bash
npm publish
```

These instructions are based on the release instructions from the [jupyter-widgets/widget-ts-cookiecutterREADME](https://github.com/jupyter-widgets/widget-ts-cookiecutter).

### Bundling the Python Package

Next, bundle the python package using

```bash
python setup.py sdist bdist_wheel
```

Then, upload the PYPI:

```bash
twine upload dist/*
```

##  Checklist after release

After releasing a new version several things need to be checked to ensure proper widget functioning.

### Check Package Managers

- https://www.npmjs.com/package/clustergrammer2 (can be slow to update)
- https://pypi.org/project/clustergrammer2/

### Check HTML Embedding
- Run `jupyter nbconvert --to html introduction_nb.ipynb` (from the examples directory) to generate a static HTML and check that the latest widget is working (uses unpkg.com)
- Check NBViewer using link to notebook on GitHub (e.g. https://nbviewer.jupyter.org/github/ismms-himc/clustergrammer2/blob/master/examples/introduction_nb.ipynb?flush_cache=true). Make sure to use the querystring `flush_cache=True` in the URL to ensure that NBVIewer re-runs nbconvert.

### Check Cloud Services
- Check MyBinder
- Check Kaggle (re-install clustergrammer2)
