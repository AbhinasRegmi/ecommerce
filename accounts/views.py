from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, TemplateView

from .forms import RegistrationForm
from .tasks import SendVerificationToken
from .models import UserBase
from .token import account_verfication_token


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
            user = form.save()

            #activation code required to send for user activation.
            #we will manage this later with celery  for now will print
            SendVerificationToken(request=self.request, user=user)
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


def activate_view(request, uid, token):
    
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = UserBase.objects.get(pk=uid_decoded)

        if user is not None and account_verfication_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()

            return HttpResponseRedirect(reverse_lazy('accounts:login'))

        return HttpResponse(content={'This activation link has expired.'})
    except:
        return HttpResponse(content={'message': 'This activation is not valid.'})