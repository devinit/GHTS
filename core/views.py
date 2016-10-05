from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from core.models import Organisation, Transaction, Contact, Sector, Currency
from csv import writer as csvwriter
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

def safeInt(x):
    try:
        return int(x)
    except:
        return -1

@login_required
def add(request):
    user = request.user
    contact = get_object_or_404(Contact,user=user)
    recipients = Transaction.RECIPIENT_CHOICES
    statuses = Transaction.PLEDGE_OR_DISB_CHOICES
    sectors = Sector.objects.all()
    channels = Transaction.DELIVERY_CHOICES
    if request.method == "POST":
        form = TransactionForm(request.POST)
        queryDict = request.POST
        year = safeInt(queryDict.get('year'))
        currencyPK = safeInt(queryDict.get('currency'))
        # print(queryDict)
        for key, value in queryDict.iteritems():
            if key != "year" and key != "currency" and safeInt(value)>0:
                meta = key.split("|")
                loan_or_grant = meta[0]
                concessional = meta[1]=="C"
                pledge_or_disbursement = meta[2]
                recipient = meta[3]
                sectorName = meta[4]
                channel_of_delivery = meta[5]
                facility = meta[6]=="F"
                transaction = Transaction()
                transaction.organisation = contact.organisation
                if year > 0:
                    transaction.year = year
                if currencyPK>0:
                    currency = Currency.objects.get(pk=currencyPK)
                    transaction.currency = currency
                transaction.loan_or_grant = loan_or_grant
                transaction.concessional = concessional
                transaction.pledge_or_disbursement = pledge_or_disbursement
                transaction.recipient = recipient
                if sectorName!="":
                    sector = Sector.objects.get(name=sectorName)
                    transaction.sector = sector
                transaction.channel_of_delivery = channel_of_delivery
                transaction.refugee_facility_for_turkey = facility
                transaction.amount = value
                transaction.save()
        return redirect('admin:core_transaction_changelist')
    else:
        form = TransactionForm()
    return render(request,'core/add.html', {"user":user,"contact":contact,"form":form,"recipients":recipients,"statuses":statuses,"sectors":sectors,"channels":channels})

@login_required
def index(request):
    user = request.user
    return render_to_response('core/home.html', {"user":user})

@login_required
def csv(request,slug):
    organisation = get_object_or_404(Organisation,slug=slug)
    transactions = Transaction.objects.filter(organisation=organisation)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+slug+'.csv"'
    writer = csvwriter(response)
    header = ["Organisation","Loan or grant","Concessional","Pledge or disbursement"
              ,"Recipient","Channel of delivery","Sector","Year","Amount","Currency"
              ,"Refugee facility for Turkey"]
    writer.writerow(header)
    for transaction in transactions:
        writer.writerow([transaction.organisation
                         ,transaction.loan_verbose()
                         ,transaction.concessional
                         ,transaction.pledge_or_disb_verbose()
                         ,transaction.recipient_verbose()
                         ,transaction.delivery_verbose()
                         ,transaction.sector
                         ,transaction.year
                         ,transaction.amount
                         ,transaction.currency
                         ,transaction.refugee_facility_for_turkey
                         ])
    return response

@login_required
def csv_all(request):
    transactions = Transaction.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'
    writer = csvwriter(response)
    header = ["Organisation","Loan or grant","Concessional","Pledge or disbursement"
              ,"Recipient","Channel of delivery","Sector","Year","Amount","Currency"
              ,"Refugee facility for Turkey"]
    writer.writerow(header)
    for transaction in transactions:
        writer.writerow([transaction.organisation
                         ,transaction.loan_verbose()
                         ,transaction.concessional
                         ,transaction.pledge_or_disb_verbose()
                         ,transaction.recipient_verbose()
                         ,transaction.delivery_verbose()
                         ,transaction.sector
                         ,transaction.year
                         ,transaction.amount
                         ,transaction.currency
                         ,transaction.refugee_facility_for_turkey
                         ])
    return response

def login_user(request):
    logout(request)
    nextURL = request.GET.get('next')
    print(nextURL)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        nextURL = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if nextURL is not None:
                  return HttpResponseRedirect(nextURL)
                else:
                  return HttpResponseRedirect('/')
    return render(request,'core/login.html', {'next':nextURL})