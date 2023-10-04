from django.urls import path
from . import views

urlpatterns =[
    path('allocate', views.AllocateIp.as_view(), name='allocate_ip'),
    path('release/<str:ip>', views.AllocateIp.as_view(), name='release ip'),
    path('allocated', views.GetAllocatedIps.as_view(), name='get_allocated_ips'),
    path('available',  views.GetAvailableIps.as_view(), name='get_available_ips'),

]