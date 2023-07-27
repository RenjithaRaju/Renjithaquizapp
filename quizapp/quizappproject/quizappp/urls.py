from django.urls import path ,include
from . import views



urlpatterns=[
  path('',views.home),
  path('register/',views.register),
  path('login/',views.login),
  path('quizdash/',views.quizdash),
  path('admindash/',views.admindash),
  path('result/',views.result),
  path('resultview/',views.resultview),
  path('downloadcsv/',views.downloadcsv),
  path('logout/',views.logout),
             
  
 
 
  

]