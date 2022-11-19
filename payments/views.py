from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutBasketForm

class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'payments/checkout.html'
    form_class = CheckoutBasketForm
    success_url = reverse_lazy('accounts:dashboard')

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'instance': self.request.user})
        return data

    def form_valid(self, form):
        return super().form_valid(form)
