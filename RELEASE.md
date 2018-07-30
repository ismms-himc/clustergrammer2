-- Latest (4-16-2018) widget publishing notes

  First, update the version numbers in the following files:

  * `package.json` then run `npm install`
  * `_version.py `
  * `example.js` and `example.py` comments

  The run the following commands in the terminal

  From the base directory:
  `$ python setup.py sdist upload -r pypi`

  from the `js` directory
  `$ npm publish`


# webpack 1.1.5
`$ node_modules/webpack/bin/./webpack.js --watch`

----------------------------------------------------------------
----------------------------------------------------------------
-- My version of pip publishing
-- http://peterdowns.com/posts/--first-time-with-pypi.html
----------------------------------------------------------------
----------------------------------------------------------------
# Update _version.py (set release version, remove 'dev')

`$ git tag -a X.X.X -m 'comment`

# ## registering has been deprecated
# (see https://packaging.python.org/guides/migrating-to-pypi-org/#uploading)
# python setup.py register -r pypitest


# to keep track of tags in GitHub
git push --follow-tags

----------------------------------------------------------------
----------------------------------------------------------------
- To release a new version of clustergrammer_glidget on NPM:
----------------------------------------------------------------
----------------------------------------------------------------

# nuke the  `dist` and `node_modules`
git clean -fdx
npm install
npm publish


----------------------------------------------------------------
----------------------------------------------------------------
-- To release a new version of clustergrammer_glidget on PyPI:
----------------------------------------------------------------
----------------------------------------------------------------

Update _version.py (set release version, remove 'dev')
git add and git commit
python setup.py sdist upload
python setup.py bdist_wheel upload
git tag -a X.X.X -m 'comment'
# Manually update _version.py (add 'dev' and increment minor)
git add and git commit
git push
git push --tags
