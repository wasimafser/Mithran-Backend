"""mithran URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

def flutter_redirect(request, resource):
    return serve(request, resource, settings.FLUTTER_WEB_DIR)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(
        'user_management/',
        include(
            'user_management.urls',
            namespace='user_management'
        )
    ),
    path(
        'service/',
        include(
            'service.urls',
            namespace='service'
        )
    ),
    path(
        'visitor_management/',
        include(
            'visitor_management.urls',
            namespace='visitor_management'
        )
    ),
    path('', lambda request: flutter_redirect(request, 'index.html')),
    path('<path:resource>', flutter_redirect),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
