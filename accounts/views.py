from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, TemplateView, View
from django.views.generic.edit import UpdateView

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, ResetYourPasswordForm, PasswordResetConfirmForm
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

class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('accounts:login'))

class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:dashboard')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


def activate_view(request, uidb64, token):
    
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid_decoded)

        if user is not None and account_verfication_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()

            return HttpResponseRedirect(reverse_lazy('accounts:login'))

        return HttpResponse(content={'This activation link has expired.'})
    except:
        return HttpResponse(content={'message': 'This activation is not valid.'})



class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/updateprofile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:dashboard')

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'instance': self.request.user})
        return data
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(request=self.request, message='Your profile has been updated successfully.')
        
        return super().form_valid(form)



class ResetYourPasswordView(PasswordResetView):
    template_name = 'accounts/passwordreset.html'
    form_class = ResetYourPasswordForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            request=self.request,
            message="Reset link has been sent to your email. Please change your password then login."
        )
        return super().form_valid(form)
    

class ResetPasswordDoneView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/passwordresetconfirm.html'
    form_class = PasswordResetConfirmForm

    def form_valid(self, form):
        messages.success(request=self.request, message='Your password was changed successfully.')
        return super().form_valid(form)