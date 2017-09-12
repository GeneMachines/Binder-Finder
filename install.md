# Installation instructions for BinderFinder

## Install Python 3.3 or greater

Download the latest standard Python 3.3+ release (not development release) from python.org.

Windows and Mac OS X users can download and run an installer.

Windows users should also install the Python for Windows extensions. Carefully read the README.txt file at the end of the list of builds, and follow its directions. Make sure you get the proper 32- or 64-bit build and Python version.

Linux users can either use their package manager to install Python 3.3+ or may build Python 3.3+ from source.

## Create directory in which to install BinderFinder

## Get project
Clone this repo into the folder using `git clone https://github.com/GeneMachines/Binder-Finder`  
Alternatively, download this repo and unzip into your directory. 

## Create a virtual environment
Using [virtualenv](https://virtualenv.pypa.io/en/stable/) set up a virtual environment in our project.
`virtualenv ~/path/to/BinderFinder`

We set an environment variable to save typing later.
`export VENV=~/path/to/BinderFinder/env`

## Install dependancies
Change directory into the root of the project where the setup.py file is and run  
`$VENV/bin/pip install -e .`

## Run BinderFinder
`$VENV/bin/pserve --reload development.ini`
