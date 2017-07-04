import sqlite3
import re
from Bio import SeqIO
from sys import argv


def seq_table_pop(c, fasta_file):
    """
    Populates the sql database seq table with embl ids and sequences.
    """
    for rec in SeqIO.parse(fasta_file, "fasta"): # for each sequence in the fasta...
        m = re.search("PN:US(\d+)", rec.description)

        if m:
            pat_id = m.group(1)
            embl_id = rec.id.split(":")[1].split("|")[0] # ...extract the embl id
            seq = str(rec.seq)

            try:
                print ("entry")
                t = (embl_id, pat_id, seq)
                c.execute("INSERT INTO seq_table (embl_id, pat_id, seq) VALUES (?,?,?)", t)
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column embl_id')
        else:
            pass


if __name__ == "__main__":

    db_h = argv[1]
    rec_h = argv[2]

    conn = sqlite3.connect(db_h)
    c = conn.cursor()

    seq_table_pop(c, rec_h)

    conn.commit()
    conn.close()
