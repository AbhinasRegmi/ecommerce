from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.conf import settings

import stripe

from .forms import CheckoutBasketForm
from orders.models import Order
from basket.basket import BasketSessions

#set the stipe api key
stripe.api_key = settings.STRIPE_SEC_KEY


#this function helps to create payment intent, and returns secret, intent
def createPaymentIntent(request):
    basket = BasketSessions(request=request)
    #from stripe api the amount must be in smallest price like paisa in NPR as int
    price = int(str(basket.getTotalPrice()).replace('.', ''))

    intent = stripe.PaymentIntent.create(
        amount=price,
        currency='npr',
        payment_method_types=["card"],
        description="Test description",
    )

    return (intent.client_secret, intent.id)

#this view function runs when checkout button is clicked, and redirects to checkout page
class PaymentIntentView(LoginRequiredMixin, RedirectView):
    pattern_name = 'payments:checkout'

    def get(self, request, *args, **kwargs):
        secret, intent = createPaymentIntent(request=self.request)
        self.request.session['client_secret'] = secret
        self.request.session['payment_intent'] = intent

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


class CSRFexemptMixin():
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFexemptMixin, self).dispatch(request, *args, **kwargs)

class PaymentConfirmationWebhook(CSRFexemptMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        event = None
        payload = self.request.body
        sig_headers = self.request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_headers,
                settings.STRIPE_HOOK_KEY
            )

            if event.type == 'charge.succeeded':
                Order.objects.filter(intent=event.data.object.payment_intent).update(billing_status=True)

        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        
        return HttpResponse(status=200)