from django.contrib import admin
from django.urls import include, path

urlpatterns = [
     path("polls/", include("polls.urls")),  # polls 앱의 URL 연결
    path("", include("polls.urls")),  # 루트 경로도 polls로 연결
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
