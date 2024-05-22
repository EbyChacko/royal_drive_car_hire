from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .forms import BookingForm
from cars.models import Car, PersonalDetails
from.models import Booking
from django.http import QueryDict
from django.contrib import messages
import stripe
import json

# Create your views here.
@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
            'mobile': request.POST.get('mobile'),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)



def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    grand_total=request.session.get('grand_total',0)
    stripe_amount = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_amount,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)
    form = BookingForm()
    car_id = request.session.get('car_id')
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request=request)
        pid = request.POST.get('client_secret').split('_secret')[0]
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                customer_details = PersonalDetails.objects.get(user=request.user)
                booking.customer = customer_details

                booking.car_id = car_id
                booking.pick_up_city = request.session.get('pick_up_city')
                booking.pick_up_county = request.session.get('pick_up_county')
                booking.drop_off_city = request.session.get('drop_off_city')
                booking.drop_off_county = request.session.get('drop_off_county')
                booking.pick_up_date = request.session.get('pick_up_date')
                booking.drop_off_date = request.session.get('drop_off_date')
                booking.pick_up_time = request.session.get('pick_up_time')
                booking.drop_off_time = request.session.get('drop_off_time')
                booking.booster_seat = request.session.get('booster_quantity', 0)
                booking.child_seat = request.session.get('childseat_quantity', 0)
                booking.infant_car_capsule = request.session.get('infant_quantity', 0)

                booking.booster_total = request.session.get('booster_total', 0)
                booking.childseat_total = request.session.get('childseat_total', 0)
                booking.infant_total = request.session.get('infant_total', 0)
                booking.total_rent = request.session.get('total_rent', 0)
                booking.grand_total = request.session.get('grand_total', 0)
                booking.days = request.session.get('days', 0)
                booking.hours = request.session.get('hours', 0)
                booking.pid = pid
                booking.save()
                return redirect('checkout_success', booking_number=booking.booking_number)
        else:
            messages.error(request, 'Fill out the form with valid values')
    else:
        if request.user.is_authenticated:
            customer_details = PersonalDetails.objects.get(user=request.user)
            form.initial = {
                'title': customer_details.title,
                'name': customer_details.name,
                'email': customer_details.user.email,
                'mobile': customer_details.mobile,
                'date_of_birth': customer_details.date_of_birth,
                'address_1': customer_details.address_1,
                'address_2': customer_details.address_2,
                'town': customer_details.town,
                'county': customer_details.county,
                'eir_code': customer_details.eir_code,
                'country': customer_details.country,
            }
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    context = {
        'car': car,
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/payment.html', context)


def checkout_success(request, booking_number):
    booking = get_object_or_404(
                                Booking, booking_number=booking_number,
                                customer__user=request.user)
    car_id = request.session.get('car_id')
    car = get_object_or_404(Car, pk=car_id)
    total_extra = booking.childseat_total + booking.infant_total + booking.booster_total
    messages.success(request,f'Booking Successfully Completed!')
    context ={
        'car':car,
        'booking' : booking,
        'total_extra' : total_extra,
    }
    return render(request, 'checkout/checkout_success.html', context)