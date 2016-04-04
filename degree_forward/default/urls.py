from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^plan/', views.plan, name='plan'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.auth, name='login'),
    url(r'^landing/', views.landing, name='landing')
]