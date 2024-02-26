from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView

from proj.middleware import AllowUnauthenticatedMixin


def get_redirect_for_user(user):
    return reverse("list_projects")


class LoginView(BaseLoginView):
    template_name = "login.jinja2"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            url = get_redirect_for_user(self.request.user)
            return HttpResponseRedirect(url)
        else:
            return super().get(request, *args, **kwargs)


class RootView(AllowUnauthenticatedMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse("login")

        else:
            return get_redirect_for_user(self.request.user)
