from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('monument/<int:monument_id>/', views.monument_detail, name='monument_detail'),
    path('panorama/<int:panorama_id>/', views.panorama_view, name='panorama_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)