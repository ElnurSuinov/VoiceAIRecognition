from django.urls import path
from AIapp.api.views import home_page, voice_api, confirm_2fa_api

urlpatterns = [
    path("", home_page, name="home"),
    path("api/voice/", voice_api, name="voice_api"),
    path("api/confirm-2fa/", confirm_2fa_api, name="confirm_2fa"),
]