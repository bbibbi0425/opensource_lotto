from django.urls import path
from . import views

urlpatterns = [
    path("", views.lotto_page, name="lotto_page"),  # 기본 경로로 lotto_page View 연결
]

