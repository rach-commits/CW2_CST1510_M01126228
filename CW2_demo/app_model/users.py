def add_user(conn, name, hash, role):
    cur = conn.cursor()
    sql= '''INSERT INTO users (username,password_hash,role) VALUES(?, ?, ?)'''
    param = (name,hash,role)
    cur.execute(sql, param)
    conn.commit()



def migrate_users(conn):
    with open('CW2_demo/DATA/users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        name, hash, role = user.strip().split(',')
        add_user(conn, name, hash, role)



def get_all_users(conn):
    cur = conn.cursor()
    sql = ''''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()
    return users


def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql,param)
    user = cur.fetchone()
    conn.close()
    return(user)


# Update just one user based on name
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql ='UPDATE users SET username = ? WHERE username = ?'
    param = (new_name, old_name)
    cur.execute(sql, param)
    conn.commit()

def delete_user(conn, user_name):
    cur = conn.cursor()
    sql='DELETE FROM users WHERE username = ?'
    param=(user_name)
    cur.execute(sql, param)
    conn.commit()