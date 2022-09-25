import sqlite3

from create_npi_db import NPI_DB

if __name__ == "__main__":

    conn = sqlite3.connect(NPI_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM npi_data WHERE lower(city)='houston'")
    result = c.fetchall()
    print(result[:2])
    print(len(result))
    # another query
    c.execute("SELECT * FROM npi_data GROUP BY city, state")
    result = c.fetchall()
    print(result[:2])
    print(len(result))
    conn.close()