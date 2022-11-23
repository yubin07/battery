from django.shortcuts import render
from django.http import request
from app.models import nasa_data
#from app.models import real_time
# Create your views here.

def index(request):
  return render(request, 'index.html')


def nasa(request):
  return render(request, 'nasa.html')

def realtime(request):
  return render(request, 'realtime.html')

def main(request):
  if request.method == 'POST':
    
    q_capacity=float(request.POST.get('capacity'))
    a_battery=nasa_data.objects.get(id=1).capacity
    soh=round((q_capacity/a_battery)*100,2)
    return render(request,'main.html',{'soh' :soh })
  
  else:
    return render(request,'main.html')




