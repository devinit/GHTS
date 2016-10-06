from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from core.models import Organisation, Transaction, Contact, Sector, Currency, Spreadsheet, Entry
from csv import writer as csvwriter
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import SpreadsheetForm

def safeInt(x):
    try:
        return int(x)
    except:
        return -1
    
def safeFloat(x):
    try:
        return float(x)
    except:
        return -1.00

@login_required
def edit(request,year):
    user = request.user
    contact = get_object_or_404(Contact,user=user)
    organisation = contact.organisation
    recipients = Transaction.RECIPIENT_CHOICES
    statuses = Transaction.PLEDGE_OR_DISB_CHOICES
    sectors = Sector.objects.all()
    channels = Transaction.DELIVERY_CHOICES
    years = Transaction.YEAR_CHOICES
    year = int(year)
    if request.method == "POST":
        form = SpreadsheetForm(request.POST)
        queryDict = request.POST
        comment = queryDict.get('comment')
        currencyPK = safeInt(queryDict.get('currency'))
        if not Spreadsheet.objects.filter(organisation=organisation,year=year).exists():
            spreadsheet = Spreadsheet()
            spreadsheet.year = year
            spreadsheet.organisation = organisation
            if currencyPK>0:
                currency = Currency.objects.get(pk=currencyPK)
            else:
                currency = Currency.objects.all()[0]
            spreadsheet.currency = currency
            spreadsheet.comment = comment
            spreadsheet.save()
        else:
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year=year)
        excludeKeys = ["currency","comment","csrfmiddlewaretoken"]
        for key, value in queryDict.iteritems():
            if Entry.objects.filter(spreadsheet=spreadsheet,coordinates=key).exists():
                entry = Entry.objects.get(spreadsheet=spreadsheet,coordinates=key)
                if safeFloat(value)>0:
                    entry.amount = value
                    entry.save()
                else:
                    entry.delete()
            elif key not in excludeKeys and value!="":
                entry = Entry()
                entry.spreadsheet = spreadsheet
                entry.coordinates = key
                if safeFloat(value)>0:
                    entry.amount = value
                    entry.save()
        return redirect(spreadsheet)
    else:
        if Spreadsheet.objects.filter(organisation=organisation,year=year).exists():
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year=year)
            form = SpreadsheetForm(instance=spreadsheet)
            entries = Entry.objects.filter(spreadsheet=spreadsheet)
        else:
            form = SpreadsheetForm()
            entries = []
    return render(request,'core/edit.html', {"user":user,"contact":contact,"form":form,"entries":entries,"recipients":recipients,"statuses":statuses,"sectors":sectors,"channels":channels,"years":years,"selected_year":year})

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