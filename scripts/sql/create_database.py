import sqlite3


def init_database(database_file):
    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()


    # Creating the sequence table
    c.execute('CREATE TABLE sequence ('
              '"seqID" VARCHAR(25) NOT NULL, '
              '"emblID" VARCHAR(25), '
              '"patID" INTEGER NOT NULL, '
              'seq VARCHAR NOT NULL, '
              'CONSTRAINT pk_sequence PRIMARY KEY ("seqID"))'
              )


    #creating the domain table
    c.execute('CREATE TABLE domain ('
              '"domainID" INTEGER NOT NULL, '
              '"pfamID" INTEGER, '
              '"emblID" VARCHAR(25) NOT NULL, '
              'CONSTRAINT pk_domain PRIMARY KEY ("domainID"))'
              )

    #creating the domain table
    c.execute('CREATE TABLE searches ('
              'id VARCHAR(50) NOT NULL, '
              'keywords VARCHAR(255) NOT NULL, '
              'pfams VARCHAR(255) NOT NULL, '
              'CONSTRAINT pk_searches PRIMARY KEY (id))'
              )

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()


if __name__ == '__main__':
    database_file = input('input path for database to create: ')
    init_database(database_file)
