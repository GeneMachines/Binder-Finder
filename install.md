# Installation instructions for BinderFinder

## Install Python 3.3 or greater

Download the latest standard Python 3.3+ release (not development release) from [python.org](https://www.python.org/downloads/).

## Create directory in which to install BinderFinder  
`mkdir ~/path/to/dir/BinderFinder`

## Get project
Clone this repo into the folder using  
`git clone https://github.com/GeneMachines/Binder-Finder`  
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
