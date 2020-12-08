from django.urls import path
from . import views

urlpatterns =[

path('',views.index,name='index'),
path('ajax/predictnumber/',views.predict_number,name='predict_number'),
path('ajax/storedata/',views.store_data,name='store_data')

]
