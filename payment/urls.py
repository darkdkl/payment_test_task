from django.conf.urls import url
from . import views

app_name = 'payment'

urlpatterns = [
    url('', views.index,name="index_pay"),

]