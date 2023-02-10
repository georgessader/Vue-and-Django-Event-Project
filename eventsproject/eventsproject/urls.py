"""eventsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signUpRequest,name="signup"),
    path('login', views.loginRequest,name="login"),
    path('home', views.createEvent,name="home"),
    path('myevents', views.getMyEvents,name="myevents"),
    path('editevent', views.editMyEvent,name="editevent"),
    path('deleteevent', views.deleteMyEvent,name="deleteevent"),
    path('events', views.getEvents,name="events"),
    path('subscribeevent', views.subscribeEvent,name="subscribeevent"),
    path('unsubscribeevent', views.unSubscribeEvent,name="unsubscribeevent"),
    path('getsubscribers', views.getSubscribers,name="getsubscribers"),
    path('getusers', views.getUsersSU,name="getusers"),
    path('clearsuperuser', views.clearUsersSU,name="clearsuperuser"),
    path('makesuperuser', views.makeUsersSU,name="makesuperuser")
]
