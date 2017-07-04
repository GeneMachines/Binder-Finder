import sqlite3
from sys import argv


def embl_table_pop(c, data):
    """                                                                                                
    Populates the sql embl table with embl ids, pfam numbers and a unique id.                          
    """
    for line in open(data, "r").readlines():
        # do work on line to get values                                                                
        t = tuple(line.strip().split("\t"))
        try:
            c.execute("INSERT INTO domain_table (domain_id, embl_id, pfam)"
                      "VALUES (?,?,?)", t)
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column embl_ids')


if __name__ == "__main__":

    db_h = argv[1]
    in_h = argv[2]

    conn = sqlite3.connect(db_h)
    c = conn.cursor()

    embl_table_pop(c, in_h)

    conn.commit()
    conn.close()
