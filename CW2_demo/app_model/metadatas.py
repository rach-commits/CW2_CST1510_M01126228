import pandas as pd

def migrate_datasets_metadata(conn):
    data = pd.read_csv('CW2_demo/DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn)
    conn.close()


def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)