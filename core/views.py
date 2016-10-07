from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from core.models import Organisation, Contact, Sector, Currency, Spreadsheet, Entry
from csv import writer as csvwriter
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import SpreadsheetForm
from .util import *

@login_required
def edit(request,year):
    facility_years = [2016,2017]
    user = request.user
    contact = get_object_or_404(Contact,user=user)
    organisation = contact.organisation
    recipients = Entry.RECIPIENT_CHOICES
    statuses = Entry.PLEDGE_OR_DISB_CHOICES
    sectors = Sector.objects.all()
    channels = Entry.DELIVERY_CHOICES
    years = Spreadsheet.YEAR_CHOICES
    year = int(year)
    if request.method == "POST":
        form = SpreadsheetForm(request.POST)
        queryDict = request.POST
        comment = queryDict.get('comment')
        if not Spreadsheet.objects.filter(organisation=organisation,year=year).exists():
            spreadsheet = form.save(commit=False)
            spreadsheet.year = year
            spreadsheet.organisation = organisation
            spreadsheet.save()
        else:
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year=year)
            form = SpreadsheetForm(request.POST,instance=spreadsheet)
            spreadsheet = form.save()
        excludeKeys = ["currency","comment","csrfmiddlewaretoken"]
        for key, value in queryDict.iteritems():
            if Entry.objects.filter(spreadsheet=spreadsheet,coordinates=key).exists():
                entry = Entry.objects.get(spreadsheet=spreadsheet,coordinates=key)
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save()
                else:
                    entry.delete()
            elif key not in excludeKeys and value!="":
                entry = Entry()
                entry.spreadsheet = spreadsheet
                entry.coordinates = key
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save()
        return redirect(spreadsheet)
    else:
        if Spreadsheet.objects.filter(organisation=organisation,year=year).exists():
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year=year)
            form = SpreadsheetForm(instance=spreadsheet)
            entries = Entry.objects.filter(spreadsheet=spreadsheet)
            currency = spreadsheet.currency
        else:
            form = SpreadsheetForm()
            entries = []
            currency = []
    return render(request,'core/edit.html', {"user":user,"contact":contact,"form":form,"entries":entries,"recipients":recipients,"statuses":statuses,"sectors":sectors,"channels":channels,"years":years,"selected_year":year,"currency":currency,"facility_years":facility_years})

@login_required
def index(request):
    user = request.user
    return render_to_response('core/home.html', {"user":user})

@login_required
def csv(request,slug):
    organisation = get_object_or_404(Organisation,slug=slug)
    spreadsheets = Spreadsheet.objects.filter(organisation=organisation)
    entries = Entry.objects.filter(spreadsheet__in=spreadsheets)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+slug+'.csv"'
    writer = csvwriter(response)
    header = ["Organisation","Loan or grant","Concessional","Pledge or disbursement"
              ,"Recipient","Sector","Channel of delivery","Year","Amount","Currency"
              ,"Refugee facility for Turkey","Comment"]
    writer.writerow(header)
    for entry in entries:
        year = entry.spreadsheet.year
        comment = entry.spreadsheet.comment
        currency = entry.spreadsheet.currency
        writer.writerow([organisation
                         ,entry.loan_or_grant()
                         ,entry.concessional()
                         ,entry.pledge_or_disbursement()
                         ,entry.recipient()
                         ,entry.sectorName()
                         ,entry.channel_of_delivery()
                         ,year
                         ,entry.amount
                         ,currency
                         ,entry.facility()
                         ,comment
                         ])
    return response

@login_required
def csv_all(request):
    entries = Entry.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'
    writer = csvwriter(response)
    header = ["Organisation","Loan or grant","Concessional","Pledge or disbursement"
              ,"Recipient","Sector","Channel of delivery","Year","Amount","Currency"
              ,"Refugee facility for Turkey","Comment"]
    writer.writerow(header)
    for entry in entries:
        organisation = entry.spreadsheet.organisation
        year = entry.spreadsheet.year
        comment = entry.spreadsheet.comment
        currency = entry.spreadsheet.currency
        writer.writerow([organisation
                         ,entry.loan_or_grant()
                         ,entry.concessional()
                         ,entry.pledge_or_disbursement()
                         ,entry.recipient()
                         ,entry.sectorName()
                         ,entry.channel_of_delivery()
                         ,year
                         ,entry.amount
                         ,currency
                         ,entry.facility()
                         ,comment
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