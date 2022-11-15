from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .forms import RegistrationForm

class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('accounts:dashboard'))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # the default behaviour is to call form.save() and return httpresponse.

        if form.is_valid():
            form.save()

            #activation code required to send for user activation.
            #we will manage this later with celery  for now will print
            #the url in terminal and activate user for testing
            messages.success(request=self.request, message='Please check your email for your account verification link. You cannot login unless you are verified.')

            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request=self.request, message='Please ensure the fields are correct.')
            return redirect(reverse_lazy('accounts:registration'))


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'