import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()
from app.models import real_time


def real_graph(request):
    real_time_df = pd.DataFrame(list(real_time.objects.all().values()))
    
    x=np.arange(0,387)
    y=real_time_df.cell_1
    y1=real_time_df.cell_2

    plt.plot(x,y)
    plt.plot(x,y1)

    plt.savefig('C:/Users/82103/Desktop/battery/battery_venv/Scripts/mysite/app/static/assets/graph/foo.png')
