import pandas as pd

def migrate_it_tickets(conn):
    data = pd.read_csv('CW2_demo/DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn)
    conn.close()


def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)