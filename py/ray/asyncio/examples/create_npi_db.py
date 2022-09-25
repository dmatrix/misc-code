import sqlite3
import os

#
# Source for this code & data: https://github.com/shantnu/Open-Gigabyte-File-Python
#

from utils import NPI_FILE_CSV, NPI_DB

def fetch_npi_data():
    counter = 0
    db_list = []
    with open(NPI_FILE_CSV) as infile:
        for line in infile:
            line = line.replace('"', '')
            data = line.split(",")
            if counter > 0:
                city = data[22]
                state = data[23]
                name = data[6] + " " + data[7] + " " + data[5]
                legal_name = data[4]
                db_list.append( (name, legal_name, city, state))
            counter += 1   
    print(len(db_list))
    return db_list
    
if __name__ == "__main__":
    if not os.path.isfile(NPI_DB):
        conn = sqlite3.connect(NPI_DB)
        c = conn.cursor()
        c.execute("CREATE TABLE npi_data (name TEXT, legal_name TEXT, city TEXT, state TEXT)")
        conn.commit()
    
    # read the huge file and fetch the list of values for insertion
    insert_lst = fetch_npi_data()
    c.executemany("INSERT INTO npi_data VALUES (?, ?, ?, ?)", insert_lst)
    conn.commit()
    conn.close()


