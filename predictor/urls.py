from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_disease, name='predict_disease'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('photos/', views.photo_list, name='photo_list'),

]
