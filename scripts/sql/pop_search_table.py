import sqlite3

def patent_table_pop(sql_cursor, pat_abst, pat_num, pat_title):
    """
    Populates a temp table with the results from the patentview text search.
    """
    
    # creates a tuple for insertion into the sql query string
    t = (pat_num, pat_title, pat_abst)
    try:
        return sql_cursor.execute("INSERT INTO patent_table"
                                  " (pat_id, pat_title, pat_desc)"
                                  "VALUES (?,?,?)", t)
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in PRIMARY KEY column pat_id')


def create_temp_table(cursor, response):
    """
    Takes the sql cursor and a search response object and creates a temporary 
    database popluating it with the search results. 
    """
    table = False
    if not table:
        # create temp table
        sql_query = ("CREATE TEMPORARY TABLE patent_table"
                     "(pat_id INTEGER PRIMARY KEY,"
                     "pat_title TEXT,"
                     "pat_desc TEXT)")
        cursor.execute(sql_query)
        table = True

    # populate the table with search results
    for patent in response.json()["patents"]: 
        patent_table_pop(cursor, *patent.values())

