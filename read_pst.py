from libratom.lib.pff import PffArchive
from email import generator
from pathlib import Path
import time
import mysql.connector
import pymysql

def connect_to_db():
    # Connection details for the first server (1.1.1.1.1.1)
    intermediary_host = '37.27.52.55'
    intermediary_user = 'dolveramails'
    intermediary_password = 'AUQABgWGB4yCAgGEAAYFhgeMggIBxAAG'
    intermediary_database = 'email_archyve'

    # Connect to the first server
    intermediary_connection = pymysql.connect(host=intermediary_host, user=intermediary_user,
                                              password=intermediary_password, database=intermediary_database)

    # Retrieve the connection details for the second server (2.2.2.2.2)
    cursor = intermediary_connection.cursor()
    cursor.execute("SELECT 192.168.56.55, dolveramails, AUQABgWGB4yCAgGEAAYFhgeMggIBxAAG, email_archyve FROM server_mapping WHERE id = 1")
    actual_host, actual_user, actual_password, actual_database = cursor.fetchone()

    # Close the connection to the first server
    intermediary_connection.close()

    # Connect to the second server
    actual_connection = pymysql.connect(host=actual_host, user=actual_user,
                                        password=actual_password, database=actual_database)
    return 1
cur = connect_to_db()
sql = "SELECT * FROM ac_directories"
cur.execute(sql)

def save_eml(pstName):
    archive = PffArchive(pstName)
    eml_out = Path(Path.cwd() / "emls")
    if not eml_out.exists():
      eml_out.mkdir()
    for folder in archive.folders():
        if folder.get_number_of_sub_messages() != 0:
            for message in folder.sub_messages:
                name = message.subject.replace(" ", "_")
                name = name.replace("/","-")
                filename = eml_out / f"{message.identifier}_{name}.eml"
                filename.write_text(archive.format_message(message))
                emailId = (message.identifier)

time.sleep(5)
save_eml('test.pst')

