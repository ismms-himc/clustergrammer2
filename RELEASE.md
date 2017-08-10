----------------------------------------------------------------
----------------------------------------------------------------
-- My version of pip publishing
-- http://peterdowns.com/posts/--first-time-with-pypi.html
----------------------------------------------------------------
----------------------------------------------------------------
# Update _version.py (set release version, remove 'dev')

git tag -a X.X.X -m 'comment'

## registering has been deprecated
(see https://packaging.python.org/guides/migrating-to-pypi-org/#uploading)
python setup.py register -r pypitest

python setup.py sdist upload -r pypitest

# to keep track of tags in GitHub
git push --follow-tags

----------------------------------------------------------------
----------------------------------------------------------------
- To release a new version of clustergrammer_widget on NPM:
----------------------------------------------------------------
----------------------------------------------------------------

# nuke the  `dist` and `node_modules`
git clean -fdx
npm install
npm publish


----------------------------------------------------------------
----------------------------------------------------------------
-- To release a new version of clustergrammer_widget on PyPI:
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
