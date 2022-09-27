
NPI_FILE_CSV = "data/npidata_pfile_20050523-20220911.csv"
NPI_DB = "data/npi_data.db"

SQL_QUERIES = ["SELECT * FROM npi_data WHERE lower(city)='houston'",
               "SELECT * FROM npi_data GROUP BY city",
               "SELECT * FROM npi_data WHERE lower(city)='boston'",
               "SELECT * FROM npi_data GROUP BY city, state",
               "SELECT * FROM npi_data WHERE lower(city)='athens' and state='TX'",
               "SELECT * FROM npi_data GROUP BY city, state, name",
               "SELECT * FROM npi_data WHERE lower(city)='athens'",
               "SELECT * FROM npi_data GROUP BY city, state, name, legal_name",
               "SELECT * FROM npi_data WHERE lower(city)='new york'",
               "SELECT * FROM npi_data"
]