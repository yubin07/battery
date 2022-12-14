import sys
import json
import django
import glob
sys.path.append('.')
from django import forms
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic import View
from django.shortcuts import render
from django.http import request,HttpResponse
from .serializer import RealSerializer,NasaSerializer,MySerializer
from app.models import nasa_data
from app.models import real_time
from app.models import capacity
import os.path   
from django.shortcuts import render
# Create your views here.

global test_input_val
test_input_val = '0.5'

def set_input(inp):
  global test_input_val
  test_input_val= str(inp)
  
def return_input():
  return test_input_val


def index(request):
  return render(request, 'index.html')

def main(request):
  return render(request,'main.html')

def lstm_nasa(test_size_val):
  import pandas as pd
  import matplotlib.pyplot as plt
  from django.http import request
  import seaborn as sns
  import os
  import tensorflow as tf
  data = pd.read_csv('static/assets/B0005.csv')
  df = pd.DataFrame(data)
  size=df['cycle'].size
  cycle=df['cycle'][size-2]

  from sklearn.preprocessing import MinMaxScaler

  scaler = MinMaxScaler()
  # 스케일을 적용할 column을 정의합니다.
  scale_cols = ['voltage_measured', 'current_measured', 'temperature_measured', 'time', 'capacity']
  # 스케일 후 columns
  scaled = scaler.fit_transform(df[scale_cols])

  df = pd.DataFrame(scaled, columns=scale_cols)

  from sklearn.model_selection import train_test_split
  x_train, x_test,y_train, y_test = train_test_split(df.drop('capacity', 1), df['capacity'], test_size=test_size_val, random_state=0, shuffle=False)

  def windowed_dataset(series, window_size, batch_size, shuffle):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    if shuffle:
      ds = ds.shuffle(1000)
    ds = ds.map(lambda w: (w[:-1], w[-1]))
    return ds.batch(batch_size).prefetch(1)

  WINDOW_SIZE=20
  BATCH_SIZE=32

  # trian_data는 학습용 데이터셋, test_data는 검증용 데이터셋 입니다.
  #train_data = windowed_dataset(y_train, WINDOW_SIZE, BATCH_SIZE, True)
  test_data = windowed_dataset(y_test, WINDOW_SIZE, BATCH_SIZE, False)

  model = tf.keras.models.load_model('static/assets/nasa_model.h5')
  pred = model.predict(test_data)
  pred.shape

  a=len(df['capacity'])-len(pred)

  copy=[None]*a
  for i in range(len(pred)):
    copy.append(pred[i][0])
  
  rest_cycle=cycle*(len(pred)/len(df))

  return pred,copy,df,cycle,y_test,rest_cycle

def lstm_my(test_size_val):
  import pandas as pd
  import matplotlib.pyplot as plt
  from django.http import request
  import seaborn as sns
  import os
  import tensorflow as tf
  data = pd.read_csv('static/assets/processed_bmsdata_cell_03.csv')
  df = pd.DataFrame(data)
  size=df['cycle'].size
  cycle=df['cycle'][size-2]

  from sklearn.preprocessing import MinMaxScaler

  scaler = MinMaxScaler()
  # 스케일을 적용할 column을 정의합니다.
  scale_cols = ['time','voltage_measured','cycle','current_measured','capacity']
  # 스케일 후 columns
  scaled = scaler.fit_transform(df[scale_cols])

  df = pd.DataFrame(scaled, columns=scale_cols)

  from sklearn.model_selection import train_test_split
  #x_train, x_test,y_train, y_test = train_test_split(df.drop('capacity', 1), df['capacity'], test_size=0.5, random_state=0, shuffle=False)
  x_train, x_test,y_train, y_test = train_test_split(df.drop('capacity', 1), df['capacity'], test_size=test_size_val, random_state=0, shuffle=False)
  
  def windowed_dataset(series, window_size, batch_size, shuffle):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    if shuffle:
      ds = ds.shuffle(1000)
    ds = ds.map(lambda w: (w[:-1], w[-1]))
    return ds.batch(batch_size).prefetch(1)

  WINDOW_SIZE=20
  BATCH_SIZE=32

  # trian_data는 학습용 데이터셋, test_data는 검증용 데이터셋 입니다.
  train_data = windowed_dataset(y_train, WINDOW_SIZE, BATCH_SIZE, True)
  test_data = windowed_dataset(y_test, WINDOW_SIZE, BATCH_SIZE, False)
  #test_data_u = windowed_dataset(y_test_u, WINDOW_SIZE, BATCH_SIZE, False)


  model = tf.keras.models.load_model('static/assets/bms_model.h5')
  pred = model.predict(test_data)
  

  a=len(df['capacity'])-len(pred)

  copy=[None]*a
  for i in range(len(pred)):
    copy.append(pred[i][0])
  
  rest_cycle=cycle*(len(pred)/len(df))

  return pred,copy,df,cycle,y_test,rest_cycle


class nasaView(APIView):
  def get(self,request):
    full_capacity = float(2.8) 
    k = float(test_input_val)
    
    test_size = ( k-( full_capacity * 0.7)) / (full_capacity - (full_capacity * 0.7))
    pred,copy,df,cycle,y_test,rest_cycle=lstm_nasa(test_size)
    data = {
      'y_test_20' : np.asarray(y_test)[20:],
      'y_test_50' : np.asarray(y_test),
      'copy' : copy,
      'pred' : pred,
      'df' : df,
      'cycle' : cycle,
      'rest_cycle' : rest_cycle,
    }
    
    return Response(data)
  
  def post(self,request):
    full_capacity = float(2.8) 
    k = float(test_input_val)
    
    test_size = ( k-( full_capacity * 0.7)) / (full_capacity - (full_capacity * 0.7))
    pred,copy,df,cycle,y_test,rest_cycle=lstm_nasa(test_size)
    data = {
      'y_test_20' : np.asarray(y_test)[20:],
      'y_test_50' : np.asarray(y_test),
      'copy' : copy,
      'pred' : pred,
      'df' : df,
      'cycle' : cycle,
      'rest_cycle' : rest_cycle,
    }
    
    return Response(data)

class nasa(View):
  def get(self, request):
    print('def get')
    global test_input_val 
    test_input_val = '2.38'
    return render(request, 'nasa.html')
  
  def post(self, request):
    print('def post')
    print(request.POST.get('a'))
    global test_input_val 
    test_input_val = request.POST.get('a')
    return render(request, 'nasa.html')

class BatteryStateView(APIView):
  def get(self, request):
    
        states = real_time.objects.all().order_by('id')

        cell1_list=[]

        cell2_list=[]
        cell3_list=[]
        cell4_list=[]
        cell5_list=[]
        cell6_list=[]
        cell7_list=[]
        cell8_list=[]
        cell9_list=[]
        cell10_list=[]
        for state in states:          
          cell1_list.append([(state.id-1)*5, state.cell_1])
          cell2_list.append([(state.id-1)*5, state.cell_2])
          cell3_list.append([(state.id-1)*5, state.cell_3])
          cell4_list.append([(state.id-1)*5, state.cell_4])
          cell5_list.append([(state.id-1)*5, state.cell_5])
          cell6_list.append([(state.id-1)*5, state.cell_6])
          cell7_list.append([(state.id-1)*5, state.cell_7])
          cell8_list.append([(state.id-1)*5, state.cell_8])
          cell9_list.append([(state.id-1)*5, state.cell_9])
          cell10_list.append([(state.id-1)*5, state.cell_10])
        data = {
            'cell_1': cell1_list,
            'cell_2': cell2_list,
            'cell_3': cell3_list,
            'cell_4': cell4_list,
            'cell_5': cell5_list,
            'cell_6': cell6_list,
            'cell_7': cell7_list,
            'cell_8': cell8_list,
            'cell_9': cell9_list,
            'cell_10': cell10_list,

        }
        return Response(data)
  def post(self,request):
    state_serializer = RealSerializer(data=request.data) #Request의 data를 stateSerializer로 변환

    if state_serializer.is_valid():
        state_serializer.save() 
        return Response(state_serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
    else:
        return Response(state_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class realtime(View):
    def get(self, request):
        return render(request, 'realtime.html')


'''
def cal(request):
  if request.method == "POST":
    full_capacity = float(2.8) 
    user_capacity=request.POST.get('a')
    k=float(user_capacity)
    print(k)
    test_size_val = ( k-( full_capacity * 0.7)) / (full_capacity - (full_capacity * 0.7))
    return test_size_val
'''

class myView(APIView):
  def get(self,request):
    full_capacity = float(2.8) 
    k = float(test_input_val)
    
    test_size = ( k-( full_capacity * 0.7)) / (full_capacity - (full_capacity * 0.7))
    pred,copy,df,cycle,y_test,rest_cycle=lstm_my(test_size)
    data = {
      'y_test_20' : np.asarray(y_test)[20:],
      'y_test_50' : np.asarray(y_test),
      'copy' : copy,
      'pred' : pred,
      'df' : df,
      'cycle' : cycle,
      'rest_cycle' : rest_cycle,
    }
    
    return Response(data)
  
  def post(self,request):
    full_capacity = float(2.8) 
    k = float(test_input_val)
    
    test_size = ( k-( full_capacity * 0.7)) / (full_capacity - (full_capacity * 0.7))
    pred,copy,df,cycle,y_test,rest_cycle=lstm_my(test_size)
    data = {
      'y_test_20' : np.asarray(y_test)[20:],
      'y_test_50' : np.asarray(y_test),
      'copy' : copy,
      'pred' : pred,
      'df' : df,
      'cycle' : cycle,
      'rest_cycle' : rest_cycle,
    }
    
    return Response(data)

class mydataView(View):
  #print(View)
  def get(self, request):
    print('def get')
    global test_input_val 
    test_input_val = '2.38'
    return render(request, 'mydata.html')
  
  def post(self, request):
    print('def post')
    print(request.POST.get('a'))
    global test_input_val 
    test_input_val = request.POST.get('a')
    return render(request, 'mydata.html')











