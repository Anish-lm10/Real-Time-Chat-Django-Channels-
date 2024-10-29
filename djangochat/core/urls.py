from django.urls import path

from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('log_in/',log_in,name='log_in'),
    path('signup/',signup,name='signup'),
    path('log_out/',log_out,name='log_out'),
    path('rooms/',rooms,name='rooms'),
    path('<slug:slug>/',room,name='room'),
]
