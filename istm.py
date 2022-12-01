import os.path   
#file = 'battery/static/assets/img/1_up.png'
#if os.path.isfile(file):
from django.shortcuts import render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.http import request
import seaborn as sns
import warnings
import os
import csv
from pandas import Series, DataFrame
import sys
import tensorflow as tf

if __name__ == "__main__":

  data = pd.read_csv('static/assets/B0005.csv')
  df = pd.DataFrame(data)

  from sklearn.preprocessing import MinMaxScaler

  scaler = MinMaxScaler()
  # 스케일을 적용할 column을 정의합니다.
  scale_cols = ['voltage_measured', 'current_measured', 'temperature_measured', 'time', 'capacity']
  # 스케일 후 columns
  scaled = scaler.fit_transform(df[scale_cols])

  df = pd.DataFrame(scaled, columns=scale_cols)

  from sklearn.model_selection import train_test_split
  x_train, x_test, y_train, y_test = train_test_split(df.drop('capacity', 1), df['capacity'], test_size=0.2, random_state=0, shuffle=False)

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

  model = tf.keras.models.load_model('static/assets/simple_model.h5')
  pred = model.predict(test_data)
  np.save('static/assets/pred',pred)

  plt.figure(figsize=(12, 9))
  plt.plot(np.asarray(y_test)[20:], label='actual', color='blue')
  plt.plot(pred, label='prediction', color='red')
  plt.ylabel('capacity')
  plt.xlabel('time')
  plt.legend()
  plt.show()
  plt.close()


  a=len(df['capacity'])-len(pred)

  copy=[None]*a
  for i in range(len(pred)):
    copy.append(pred[i][0])

  plt.figure(figsize=(12,9))
  plt.plot(df['capacity'], label='actual', color='blue')
  plt.plot(copy, label='prediction', color='red')
  plt.ylabel('capacity')
  plt.xlabel('time')
  plt.legend()
  plt.show()
  plt.close()
else:
 pass


