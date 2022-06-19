from django.urls import path
from .views import home,students,main,GeneratePDF
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [

    path('',home,name='home'),
    path('students/',students,name="students"),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('main/',main,name='main'),
    path('pdf/<int:id>',GeneratePDF,name='pdf'),
    
    
]