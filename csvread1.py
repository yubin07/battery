import os
import csv
import django

from app.models import nasa_data

with open('B0005.csv', encoding='utf-8') as csv_file:
       while True:
              rows = csv.reader(csv_file)
              next(rows, None)
              for row in rows:
               nasa_data.objects.create(
                voltage_measured=float(row[0]),
                current_measured=float(row[1]),
                temperature_measured=float(row[2]),
                current_load=float(row[3]),
                voltage_load=float(row[4]),
                time=float(row[5]),
                capacity=float(row[6]),
                cycle=int(row[7]),
              )

