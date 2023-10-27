PKG_VERSION = $(shell python setup.py --version)

test:
	JAX_PLATFORM_NAME=cpu pytest

# We launch the package release by tagging the master branch with the package's
# new version number. The version number is read from `blackjax/__init__.py`
release:
	git tag -a $(PKG_VERSION) -m $(PKG_VERSION)
	git push --tag

