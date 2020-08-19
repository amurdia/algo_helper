# -*- coding: utf-8 -*-
# =================================== Meta ================================== #
'''
Author: Ankit Murdia
Contributors:
Version: 0.0.1
Created: 2020-08-15 11:24:09
Updated: 2020-08-15 12:26:27
Description:
Notes:
To do:
'''
# =========================================================================== #


# =============================== Dependencies ============================== #
import setuptools
# =========================================================================== #


# ================================ Constants ================================ #

# =========================================================================== #


# ================================ Code Logic =============================== #
#  Callable methods

#  Abstracted classes

# =========================================================================== #


# ================================== Globals =================================== #
with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="algo-helper-amurdia",
	version="0.0.1",
	author="Ankit Murdia",
	description="Helper package to index and practice competitive programming problems.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/amurdia/algo_helper.git",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.8',
)
# ============================================================================== #


# =============================== CLI Handler =============================== #
if __name__ == "__main__":
    pass
# =========================================================================== #