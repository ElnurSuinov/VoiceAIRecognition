from django.urls import  path
from .views import home_page, voice_api

urlpatterns = [
       path('', home_page, name="home"),
       path('api/voice/', voice_api, name="voice_api")
]