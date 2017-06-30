import sqlite3


sqlite_file = 'foobar.sqlite'    # name of the sqlite database file
table_name1 = 'patent_table'  # name of the table to be created
table_name2 = 'seq_table'  # name of the table to be created
new_field1 = 'pat_id' # name of the column
new_field2 = 'pat_title' # name of the column
new_field3 = 'pat_desc' # name of the column
new_field4 = 'embl_id' # name of the column

text_type = 'TEXT'  # column data type
int_type = 'INTEGER' 

def init_database():
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()


    # creating tuple for string generation
    t = (table_name1, new_field1, text_type, new_field2, text_type,
         new_field3, text_type)
    # Creating a new SQLite table with 1 column
    c.execute('CREATE TABLE ? '
              '(? ? PRIMARY KEY, ? ?, ? ?)', t)

    # Creating a second table with 1 column and set it as PRIMARY KEY
    # note that PRIMARY KEY column must consist of unique values!
    t2 = (table_name2, new_field4, text_type,
          new_field1, text_type)
    c.execute('CREATE TABLE ? (? ? PRIMARY KEY, ? ?)', t2)

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()


init_database()
