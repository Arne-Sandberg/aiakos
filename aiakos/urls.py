"""project URL Configuration

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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView

from .openid_provider.views import ConfigurationView
from .views import password_change, password_reset

urlpatterns = [
	url(r'^$', login_required(RedirectView.as_view(url=settings.HOME_URL)), name='home'),
	url(r'^apps/$', login_required(TemplateView.as_view(template_name='apps.html')), name='apps'),
	url(r'^admin/', admin.site.urls),
	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/password-change/$', login_required(password_change), name="custom-password-change"),
	url(r'^accounts/password-reset/$', password_reset, name="custom-password-reset"),
	url(r'^accounts/', include('django_extauth.urls', namespace='extauth')),
	url(r'^oauth/', include('aiakos.openid_provider.urls', namespace='openid_provider')),
	url(r'^\.well-known/openid-configuration$', ConfigurationView.as_view()),
	url(r'^', include('django_profile_oidc.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
