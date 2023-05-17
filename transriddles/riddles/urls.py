from django.urls import path
from riddles import views

app_name = 'riddles'

urlpatterns = [
    path('', views.index, name='index'),
]
