from django.urls import path
from .views import StripeCheckoutView, stripe_webhook

urlpatterns = [
path('create-checkout-session/', StripeCheckoutView.as_view()),
path('webhook/', stripe_webhook, name='stripe-webhook'),
]