import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

'''from app.models import real_time

with open('L9963_data_2022_11_ 2_15_56_54_voltage.txt', encoding='utf-8') as txtfile:
       while True:
              list = txtfile.readline()
              row= list.split()
              if not list: break
              real_time.objects.create(
                     tik = row[0],
                     cell_1 = float(row[1]),
                     cell_2 = float(row[2]),
                     cell_3 = float(row[3]),
                     cell_4 = float(row[4]),
                     cell_5 = float(row[5]),
                     cell_6 = float(row[6]),
                     cell_7 = float(row[7]),
                     cell_8 = float(row[8]),
                     cell_9 = float(row[9]),
                     cell_10 = float(row[10])
              )
'''

