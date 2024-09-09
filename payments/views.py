import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Computer
from decouple import config

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            computer_id = request.data.get('computer_id')
            
            if not computer_id:
                return Response({'error': 'No computer_id provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            computer = Computer.objects.get(id=computer_id)

            if computer.quantity < 1:
                return Response({'error': 'Computer out of stock'}, status=status.HTTP_400_BAD_REQUEST)

            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': computer.model,
                            },
                            'unit_amount': int(computer.price * 100),  # Stripe expects the amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
                metadata={
                    'computer_id': computer_id
                }
            )
            return Response({'url': session.url}, status=status.HTTP_200_OK)
        except Computer.DoesNotExist:
            return Response({'error': 'Computer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = config("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': str(e)}, status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        computer_id = session['metadata']['computer_id']
        
        try:
            computer = Computer.objects.get(id=computer_id)
            if computer.quantity > 0:
                computer.quantity -= 1
                computer.save()
            else:
                return JsonResponse({'error': 'Computer out of stock'}, status=400)
        except Computer.DoesNotExist:
            return JsonResponse({'error': 'Computer not found'}, status=404)

    return JsonResponse({'status': 'success'}, status=200)