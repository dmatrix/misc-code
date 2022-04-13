import os

MONTHS = ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06']

if __name__ == '__main__':
   for month in MONTHS:
      cmd = f"pypistats python_major pyspark --month {month}"
      os.system(cmd)
