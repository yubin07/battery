import sys
sys.path.append('.')
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic import View
from django.shortcuts import render
from django.http import request
from .serializer import RealSerializer,NasaSerializer
from app.models import nasa_data
from app.models import real_time
# Create your views here.

def index(request):
  return render(request, 'index.html')

def nasa(request):
  if request.method == 'POST':
    def find_nearest(array, value):
      array = np.asarray(array)
      idx = (np.abs(array - value)).argmin()
      return array[idx]
    q_capacity=float(request.POST.get('capacity'))
    a_battery=np.load('static/assets/pred.npy')
    k=find_nearest(a_battery,q_capacity)
    
    soh=k/float(a_battery[1])
    return render(request,'nasa.html',{'soh': soh})
  
  else:
    return render(request,'nasa.html')


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
          cell1_list.append([state.id, state.cell_1])
          cell2_list.append([state.id, state.cell_2])
          cell3_list.append([state.id, state.cell_3])
          cell4_list.append([state.id, state.cell_4])
          cell5_list.append([state.id, state.cell_5])
          cell6_list.append([state.id, state.cell_6])
          cell7_list.append([state.id, state.cell_7])
          cell8_list.append([state.id, state.cell_8])
          cell9_list.append([state.id, state.cell_9])
          cell10_list.append([state.id, state.cell_10])
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
        state_serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
        return Response(state_serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
    else:
        return Response(state_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class realtime(View):
    def get(self, request):
        return render(request, 'realtime.html')

def main(request):
    return render(request,'main.html')




