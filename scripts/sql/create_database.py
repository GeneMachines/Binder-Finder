import sqlite3


def init_database(database_file):
    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()


    # Creating the sequence table
    c.execute('CREATE TABLE seq_table '
              '(embl_id TEXT PRIMARY KEY, pat_id INTEGER, seq TEXT)')

    #creating the domain table
    c.execute('CREATE TABLE domain_table '
              '(domain_id INTEGER PRIMARY KEY, embl_id TEXT, pfam INTEGER)')

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()


if __name__ == '__main__':
    database_file = input('input path for database to create: ')
    init_database(database_file)
