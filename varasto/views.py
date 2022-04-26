import operator
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserForm
from .checkUser import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from .models import User, Goods, Storage_name, Storage_place, Rental_event, Staff_event, CustomUser
from django.db.models import Count
from django.db.models.functions import TruncMonth, Trunc
from django.db.models import Min, Max



def new_item(request):
    return render(request, 'varasto/new_item.html')

def inventaario_side_window(request):
    return render(request, 'varasto/inventaario_side_window.html')

def person_view(request):
    return render(request, 'varasto/person.html')


@login_required()
@user_passes_test(is_not_student, redirect_field_name=None)
def renter(request, idx):
    selected_user = CustomUser.objects.get(id=idx)
    print(selected_user)

    now = datetime.now()
    datenow = now.strftime("%d.%m.%Y")
    context = {
        'selected_user': selected_user,
        'user': request.user,
        'idx': idx,
        'datenow': datenow,
    }
    return render(request, 'varasto/renter.html', context)

def new_event(request):
    return render(request, 'varasto/new_event.html')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('sucsess')
                if user_check(user) and is_not_student(user):
                    return redirect('rental_events')
                else:
                    return HttpResponse("<html><body><h1>Ei ole okeuksia päästä tähän sivuun</h1></body></html>") # Tässä voimme tehdä Timer, 10 sec jälkeen tehdään LOGOUT
            else:
                # Pitää rakentaa frontendilla vastaus, että kirjoitettu salasana tai tunnus oli väärin
                return redirect('login')
                # return HttpResponse("<html><body><h1>error</h1></body></html>")
        else:
            form = CustomUserForm()
            context = {'form': form}
            return render(request, 'varasto/login.html', context)
    else:
        if user_check(request.user) and is_not_student(request.user):
            return redirect('rental_events')
        else:
            return HttpResponse("<html><body><h1>Ei ole okeuksia päästä tähän sivuun</h1></body></html>") # Tässä voimme tehdä Timer, 10 sec jälkeen tehdään LOGOUT


def logout_view(request):
    logout(request)
    return redirect('login')

def recovery_view(request):
    if request.user.is_authenticated:
        return redirect('login')
    return render(request, 'varasto/recovery.html')

def index(request):
    return redirect('login')
    # if not request.user.is_authenticated:
    #     return redirect('login')
    # return render(request, 'varasto/index.html')

def user_recovery(request):
    return render(request, 'varasto/recovery.html')


def base_main(request):
    now = datetime.now()
    datenow = now.strftime("%d.%m.%Y")
    context = {
        'datenow': datenow,
        'user': request.user
    }
    return render(request, 'varasto/base_main.html', context)

def update_rental_status(request):
    return render(request, 'varasto/update_rental_status.html')

@login_required()
@user_passes_test(is_not_student, redirect_field_name=None)
def rental_events(request):
    renters_by_min_startdate = Rental_event.objects.values('renter').filter(returned_date__isnull=True).annotate(mindate=Min('start_date'))
    # grouped_events1 = renters_by_min_startdate.filter(start_date__in=renters_by_min_startdate.values('mindate')).order_by('start_date')
    events = Rental_event.objects.filter(returned_date__isnull=True).order_by('renter', 'start_date')
    grouped_events = Rental_event.objects.filter(returned_date__isnull=True).filter(start_date__in=renters_by_min_startdate.values('mindate')).order_by('start_date').distinct('start_date')

    # for i in grouped_events: 
    #     print(i)

    # for i in grouped_events: 
    #     # print(i)
    #     # print(i['renter'])
    #     print(i.renter_id, i.item, i.start_date)

    now = datetime.now()
    datenow = now.strftime("%d.%m.%Y")
    context = {
        'grouped_events': grouped_events,
        'events': events,
        'datenow': datenow,
        'user': request.user
    }

    return render(request, 'varasto/rental_events.html', context)



def new_event_goods(request):
    return render(request, 'varasto/new_event_goods.html')

def inventory(request):
    return render(request, 'varasto/inventory.html')


