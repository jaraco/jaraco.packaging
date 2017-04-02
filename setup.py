#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'jaraco.packaging'
description = 'tools to supplement packaging Python releases'

params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	install_requires=[
		'six>=1.4',
	],
	extras_require={
		':python_version=="2.6"': [
			'subprocess32',
		],
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Framework :: Sphinx :: Extension",
	],
	entry_points={
		'console_scripts': [
			'dependency-tree=jaraco.packaging.depends:tree_cmd',
			'upload-package=jaraco.packaging.cheese:do_upload',
		],
		'distutils.commands': [
			'dependency_tree=jaraco.packaging.depends:DependencyTree',
			'show=jaraco.packaging.info:Show',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
