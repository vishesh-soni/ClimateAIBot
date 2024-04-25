from django.contrib import admin
from django.urls import path
from . import views
from .views import get_answer
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home),
    path('get-answer/', get_answer, name='get_answer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)