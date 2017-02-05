from django.conf.urls import url
from .views import login_view,logout_view,dashboard,register

urlpatterns = [ 
    url(r'^login$',login_view,name='login'),
    url(r'^logout$',logout_view,name='logout'),
    url(r'^dashboard$',dashboard,name='dashboard'),
    url(r'^register$',register,name='register'),
    ]