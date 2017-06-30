import sqlite3


def join_on_search_and_domain(cursor, pfam_ids):
    """
    Takes the searched pfam domains and performs the sql query returning the 
    cursor. The query searches only those sequences whith the pfam(s) requested
    for patent numbers and then joins that with the temporary table of patents
    searched by keyword.
    """

    t = tuple(pfam_ids,)
    sql_query = (
        "SELECT seq_table.seq, search_table.* " # select data to return
        "FROM domain_table "
            "JOIN seq_table " # get sequences...
                "ON domain_table.embl_id = seq_table.embl_id "
            "JOIN search_table " # ...get patents for those sequences...
                "ON search_table.pat_id = seq_table.pat_id "
        "WHERE domain_table.pfam IN ({})".format(
            ",".join(["?"]*len(pfam_ids)))) # ...to the search
    cursor.execute(sql_query, t)

    return cursor

if __name__ == "__main__":
    f = "/Users/j.parker/working_dir/filter_binders/database/foobar.sqlite"
    conn = sqlite3.connect(f)
    c = conn.cursor()
    join_on_search_and_domain(c, ["pfam1"])

