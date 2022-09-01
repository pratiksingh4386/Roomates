from django.urls import path
from . import views

urlpatterns=[
    path('',views.roomselect,name="roomselect"),
    path('roomconfirm/<int:id>',views.roomconfirm,name="roomconfirm"),
    path('showroomate',views.showroomate,name="showroomate"),
]

