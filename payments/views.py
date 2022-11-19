from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings

import stripe

from .forms import CheckoutBasketForm
from basket.basket import BasketSessions


class PaymentIntentView(LoginRequiredMixin, RedirectView):
    pattern_name = 'payments:checkout'

    def get(self, request, *args, **kwargs):
        basket = BasketSessions(request=self.request)
        #from stripe api the amount must be in smallest price like paisa in NPR as int
        price = int(str(basket.getTotalPrice()).replace('.', ''))
        intent = stripe.PaymentIntent.create(
            api_key=settings.STRIPE_SEC_KEY,
            amount=price,
            currency='npr',
            metadata={
                'uid': self.request.user.id,
            }
        )

        self.request.session['client_secret'] = intent.get('client_secret')
        
        return super().get(request, *args, **kwargs)

class PaymentIntentCancelView(LoginRequiredMixin, RedirectView):
    pattern_name = 'basket:basket-sum-view'

    #we will implement this later.


    def get(self, request, *args, **kwargs):
        intent_id = self.request.kwargs.get('intent_id')
        stripe.PaymentIntent.cancel(intent_id)
        return super().get(request, *args, **kwargs)

class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'payments/checkout.html'
    form_class = CheckoutBasketForm
    success_url = reverse_lazy('accounts:dashboard')

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'instance': self.request.user})
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pub_key'] = settings.STRIPE_PUB_KEY
        context['success_url'] = self.get_success_url()
        return context

    def form_valid(self, form):
        return super().form_valid(form)

