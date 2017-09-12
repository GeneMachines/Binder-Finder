# Binder discovery from publicly available data
The aim of this project is to develop a semi-automated search for existing binders for particular targets. This approach will combine a sequence-based search to identify scaffolds of interest with a text based search of annotations for the target. 

## Installation instructions for BinderFinder

### Install Python 3.3 or greater

Download the latest standard Python 3.3+ release (not development release) from [python.org](https://www.python.org/downloads/).

### Create directory in which to install BinderFinder  
`mkdir ~/path/to/dir/BinderFinder`  

and move into that directory  

`cd ~/path/to/dir/BinderFinder`  

### Get project
Clone this repo into the directory using  
`git clone https://github.com/GeneMachines/BinderFinder`
Alternatively, download this repo and unzip into your directory.

### Create a virtual environment
Using [virtualenv](https://virtualenv.pypa.io/en/stable/) set up a virtual environment in our project.  
`venv ~/path/to/BinderFinder`

We set an environment variable to save typing later.  
`export VENV=~/path/to/BinderFinder/env`

### Install dependancies
Change directory into the root of the project where the setup.py file is and run  
`$VENV/bin/pip install -e .`

### Run BinderFinder
`$VENV/bin/pserve --reload development.ini`

## Design
### Functionality
Major features to be implimented in this project:

* database selection (pdb, patents, nr– dropdown)
* scaffold selection (possibly dropdown or hmm or pfam id, eg V<sub>H</sub>H/PF07686)
* annotation search (keyword input)

Other features:

* if target is a also a protein, check to see if co-crystal structure exists in pdb
* differentiate V<sub>H</sub>H from S<sub>C</sub>F<sub>V</sub>, FAB, and full-length IgG antibodies (length, presence/absence of constant domains)
* expand text search to include multiple sources (patent contents/associated papers etc.)

### Database selection
This should be the easiest to implement. Download data and set up searchable database. Select by identifier.

### Scaffold selection
This can be done in a couple of ways. If only pre-defined options exist then searches can be pre-computed and a reduced dataset provided for each scaffold selection. If the user provides an hmm or pfam id, this lookup will have to be performed on the fly using a call to hmmsearch.

Selecting for antibody subtypes could be difficult. The v-set pfam ([PF07686](pfam.xfam.org/family/PF07686)) will match any IgG-like variable region. Selecting by domain architectures might be difficult as distinguishing between truncated sequences and true antibody fragments might be impossible. The data annotations may have to be relied upon for this or the burden passed to the user. 

This assumption should be tested by building a curated model of each scaffold of interest and searching against the database, scoring the fidelity with which that specific scaffold is returned. 

### Annotation search
This will be the trickiest. Ideally an advanced search will be used which takes synonyms into account as well as misspellings. Also, what can be searched will depend on which database is being searched. There are vastly different data associated with each of the PDB and patent databases. The best solution might be to use an existing API to leverage the advanced search functionality. Examples might be the [Google search API](https://developers.google.com/custom-search/) together with the patent database flag, "&tbm=pts"; the EMBL-EBI [ENA API](https://www.ebi.ac.uk/about/news/service-news/new-ena-discovery-api); or [pyPDB](https://github.com/williamgilpin/pypdb) a python API for the RCSB PDB.

### Combining filters
#### Patent database
Patents have a unique identifier. This identifier is returned in a list by most text searches. By performing the text search via an API, the list of returned patent applications can be compared against the list of patents containing sequences of interest.  
There are multiple patent resources. EMBL-EBI provoides a database of patent sequences. Google scholar and The Lens provide searches of the patent literature. The Lens also provides some ability to access sequences associated with those patents.

#### PDB database
As above, except the unique identifier is the pdb id. 

#### IMGT antibody database
This is already a highly curated database so all that needs to be done is to perform a text search. 

