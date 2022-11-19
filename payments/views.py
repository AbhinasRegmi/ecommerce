from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/checkout.html'
