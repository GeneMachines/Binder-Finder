import sqlite3
from Bio import SeqIO


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
    for i, line in enumerate(embl_domain):
        # do work on line to get values
        t = tuple([i]+line.split(","))
        try:
            c.execute("INSERT INTO domain_table (domain_id, embl_id, pfam)" 
                      "VALUES (?,?,?)", t)
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column embl_ids')


def main():
    """
    Decides what to do depending on input. 
    """
    pass


if __name__ == '__main__':
    sqlite_file = '/Users/j.parker/working_dir/filter_binders/database/foobar.sqlite'

    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    #seq_table_pop('/Users/j.parker/data/databases/patent_data/nrp_patent_nospace.fa')
    
    embl_table_pop(open("/Users/j.parker/working_dir/filter_binders/test/embl_ids.test", "r"))

    # do search
    # populate search table / select patents based on results
    e# do join operations
    # return results

    conn.commit()
    conn.close()
