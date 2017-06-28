import sqlite3
from Bio import SeqIO


def patent_table_pop(patent_search_results):
    """
    Populates a table with the results from the patentview text search.
    """

    for patent in patent_search_results:
        t = (pat_id, pat_title, pat_desc)
        try:
            c.execute("INSERT INTO patent_table (pat_id, pat_title, pat_desc)" 
                      "VALUES (?,?,?)", t)
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


def seq_table_pop(fasta_file):
    """
    Populates the sql database seq table with embl ids and sequences.
    """
    id_column = 'embl_id'
    column_name = 'seq'
    table_name = 'seq_table'
    for rec in SeqIO.parse(fasta_file, "fasta"):
        embl_id = rec.id.split(":")[1].split("|")[0]
     
   #print (embl_id)
        try:
            c.execute("INSERT INTO seq_table (embl_id, seq)" 
                      "VALUES ((?,?)", (embl_id, rec.seq))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


def embl_table_pop(embl_domain):
    """
    Populates the sql embl table with embl ids, pfam numbers and a unique id.
    """
    for line in embl_domain:
        # do work on line to get values
        t = tuple(line.split(","))
        try:
            c.execute("INSERT INTO domain_table (domain_id, embl_id, pfam)" 
                      "VALUES (?,?,?)", t)
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))


def main():
    """
    Decides what to do depending on input. 
    """


if __name__ == '__main__':
    sqlite_file = 'foobar.sqlite'

    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    #seq_table_pop('/Users/j.parker/data/databases/patent_data/nrp_patent_nospace.fa')

    # do search
    # populate search table / select patents based on results
    # do join operations
    # return results

    conn.commit()
    conn.close()
