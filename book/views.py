from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from datetime import datetime
from book.models import Journey
import hashlib, random
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from book.forms import BookingForm
from basic.models import UserProfile
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def make_bookings(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = BookingForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()
            source_location = form.cleaned_data['source_location']
            destination_location = form.cleaned_data['destination_location']
            journey_date = form.cleaned_data['journey_date']
            number_of_tickets = form.cleaned_data['number_of_tickets']
            mode_of_transport = form.cleaned_data['mode_of_transport']
            if journey_date < datetime.now():
                return render_to_response('error.html')
            journey_query = Journey(user=request.user, source_location=source_location,
                                    destination_location=destination_location,
                                    number_of_tickets=number_of_tickets,
                                    journey_date=journey_date,
                                    mode_of_transport=mode_of_transport,
                                    )
            journey_query.save()
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            redirect_url = 'book/'+salt
            return HttpResponseRedirect(redirect_url)
    else:
        if request.user.is_authenticated():
            HttpResponseRedirect('/home')
        args['form'] = BookingForm()

    return render_to_response('home.html', args, context_instance=RequestContext(request))


def confirm_booking(request):
