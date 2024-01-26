import mysql.connector

def connect():
    cnx = mysql.connector.connect(
            user='dolveramails',
            password='AUQABgWGB4yCAgGEAAYFhgeMggIBxAAG',
            host='',
            database='email_archyve'
        )
    cur = cnx.cursor()
    cur.execute("SELECT * FROM ac_directories")
    rows = cur.fetchall()
    return rows
print(connect())