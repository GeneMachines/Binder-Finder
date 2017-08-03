import sqlite3
from search.query_patentview import *
from sql.pop_search_table import *
from sql.domain_join import *
from pprint import pprint

# query patent view database for keyword <query_string>
query_string = "albumin"
response = search_patentview(query_string, verbose=True)

pprint(response.json()['patents'][0])

# connect to sql database
f = "/Users/j.parker/working_dir/binder_finder/project/database/foobar.sqlite"
conn = sqlite3.connect(f)
c = conn.cursor()

# create a temp table of search results
c = create_temp_table(c, response)


# perform join operation to get results with only our domain of interest
pfam_ids = ["pfam1, pfam2"]
c = join_on_search_and_domain(c, pfam_ids)

#print(c.fetchall())
