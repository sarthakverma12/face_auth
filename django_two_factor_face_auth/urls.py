"""authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""



from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.face_login, name='login'),
    path('about/', views.about, name='about'),
    path('accounts/menu/', views.menu, name='menu'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/files/', views.viewfiles, name='viewfiles'),
    path('accounts/upload/', views.upload, name='upload'),
    path('accounts/fdelete/', views.fdelete, name='fdelete'),
    path('accounts/fsearch/', views.fsearch, name='fsearch'),
    path('content/<str:user>/<str:dfile>/', views.fdownload, name='fdownload'),
    path('logout/',auth_views.LogoutView.as_view(template_name='django_two_factor_face_auth/logout.html'),name='logout'),

    # path('accounts/fdownload/', views.fdownload, name='fdownload'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

