"""tangowithdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse
from rango import views
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('rango:register_profile')


urlpatterns = [
                  path('', views.index, name='index'),
                  # The following line maps any URLs staring with 'rango/' to be handled by the rango application
                  path('rango/', include('rango.urls')),
                  path('admin/', admin.site.urls),
                  path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
                  path('accounts/', include('registration.backends.simple.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# The accounts path has the following sub-URL paths
# Activity                URL                         Mapping Name
#                         /accounts...
# Login                   .../login/                  auth_login
# Logout                  .../logout/                 auth_logout
# Registration            .../register/               registration_register
# Registration Closed     .../register/closed/        registration_disallowed
# Password Change         .../password/change/        auth_password_change
# Change Complete         .../password/change/done/   auth_password_change_done
