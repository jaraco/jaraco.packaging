#!/usr/bin/env python
# Generated by jaraco.develop 2.20
# https://pypi.python.org/pypi/jaraco.develop

import io
import sys

import setuptools

with io.open('README.txt', encoding='utf-8') as readme:
	long_description = readme.read()

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_sphinx = {'release', 'build_sphinx', 'upload_docs'}.intersection(sys.argv)
sphinx = ['sphinx'] if needs_sphinx else []

setup_params = dict(
	name='jaraco.packaging',
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description="tools to supplement packaging Python releases",
	long_description=long_description,
	url="https://bitbucket.org/jaraco/jaraco.packaging",
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=['jaraco'],
	install_requires=[
		'requests',
		'six>=1.4,<2dev',
	],
	extras_require={
	},
	setup_requires=[
		'setuptools_scm',
	] + pytest_runner + sphinx,
	tests_require=[
		'pytest',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'console_scripts': [
			'dependency-tree=jaraco.packaging.depends:tree_cmd',
			'upload-package=jaraco.packaging.cheese:do_upload',
		],
		'distutils.commands': [
			'dependency_tree=jaraco.packaging.depends:DependencyTree',
		],
		'pmxbot_handlers': [
			'cheeseshop uploader=jaraco.packaging.pmxbot',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
