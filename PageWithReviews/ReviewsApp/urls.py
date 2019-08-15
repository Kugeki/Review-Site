from django.urls import path
from django.conf.urls import url
from . import views

from django.views.generic import RedirectView
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^ajax/get_response/$', views.answer_me, name='get_response'),
    url(r'^ajax/reviews_api/$', views.reviews_api, name='reviews_api'),
    path('api/', views.ReviewView.as_view(), name='api'),
]