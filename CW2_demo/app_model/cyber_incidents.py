def migrate_cyber_incidents(conn):
    data = pd.read_csv('CW2_demo/DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn)
    conn.close()

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)