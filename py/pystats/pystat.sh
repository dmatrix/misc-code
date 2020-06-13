#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 package_name" >&2
  exit 1
fi
for months in '2019-12' '2020-01' '2020-02' '2020-03' '2020-04' '2020-05' '2020-06'
do
  pypistats python_major $1 --month $months
done
