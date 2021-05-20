import sqlite3

# db_name = the name of the database
def create_table_db(db_name):
    # SQL statements
    sql_drop_entries = '''
        DELETE FROM uniqueMAC;
    '''
    sql_create_table = '''
        CREATE TABLE IF NOT EXISTS uniqueMAC(
            TX TEXT,
            RX TEXT,
            SNR REAL);
        '''   
    # connect to database
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # execute sql
    cur.execute(sql_create_table)
    cur.execute(sql_drop_entries)

    # end up execution
    con.commit()
    cur.close() 
    con.close()

def read_all_records_db(db_name):
    # SQL statements
    sql_read_record = '''
        SELECT * FROM uniqueMAC;
        '''
    # connect to database
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # execute sql
    cur.execute(sql_read_record) 
    result = cur.fetchall()
    # end up execution
    con.commit()
    cur.close() 
    con.close()
    return result

def log_results(results):
    with open('query_output','w') as f:
        for r in results:
            tx = r[0]
            rx = r[1]
            snr = r[2]
            f.write('{},{},{}'.format(tx,rx,snr))