import os

MONTHS = ['2019-12','2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06']

if __name__ == '__main__':
   for month in MONTHS:
      cmd = f"pypistats python_major pyspark --month {month}"
      os.system(cmd)
