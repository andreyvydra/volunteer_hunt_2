from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('auth/', include('user.urls')),
    path('task/', include('tasks.urls')),
    path('map/', include('map.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
