import sqlite3


sqlite_file = 'foobar.sqlite'    # name of the sqlite database file
table_name1 = 'patent_table'  # name of the table to be created
table_name2 = 'seq_table'  # name of the table to be created
new_field1 = 'pat_id' # name of the column
new_field2 = 'pat_title' # name of the column
new_field3 = 'pat_desc' # name of the column
new_field4 = 'embl_id' # name of the column

text_type = 'TEXT'  # column data type
int_type = 'INT' 

def init_database():
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Creating a new SQLite table with 1 column
    c.execute('CREATE TABLE {tn} ({nf1} {ft1} PRIMARY KEY, {nf2} {ft2}, {nf3} {ft3})'\
                  .format(tn=table_name1, 
                          nf1=new_field1, ft1=text_type, 
                          nf2=new_field2, ft2=text_type, 
                          nf3=new_field3, ft3=text_type))

    # Creating a second table with 1 column and set it as PRIMARY KEY
    # note that PRIMARY KEY column must consist of unique values!
    c.execute('CREATE TABLE {tn} ({nf1} {ft1} PRIMARY KEY, {nf2} {ft2})'\
                  .format(tn=table_name2, nf1=new_field4, ft1=text_type,
                          nf2=new_field1, ft2=text_type))

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()


init_database()
