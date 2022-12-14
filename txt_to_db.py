import os
import glob
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()
from app.models import real_time

path_dir = 'C:/Users/wkddn/capstone/bmsdata/backup'
allFile_list = glob.glob(os.path.join(path_dir, 'L9963*')) # glob함수로 L9963으로 시작하는 파일들을 모은다
#real_time.objects.all().delete()
print(allFile_list[-1])
cnt = 0
with open(allFile_list[-1], encoding='utf-8') as txtfile:
       while True:
              list = txtfile.readline()
              row= list[-1].split()
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
              time.sleep(1)
              print("refresh!")
              #if not list: break


'''
with open(allFile_list[-1], encoding='utf-8') as txtfile:
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
print(cnt)
print('done!')

