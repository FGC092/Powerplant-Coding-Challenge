from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productionplan', views.productionplan.as_view(), name='productionplan'),
]