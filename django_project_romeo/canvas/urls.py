from django.urls import path
from . import views

app_name = 'canvas'
urlpatterns = [
    path('', views.canvas_list, name='canvas-list'),
    path('new/', views.canvas_create, name='canvas-create'),
    path('<int:pk>/', views.canvas_detail, name='canvas-detail'),
    path('place_pixel/', views.place_pixel, name='place-pixel'),
    path('<int:pk>/pixels/', views.get_pixels, name='canvas-pixels'),
]