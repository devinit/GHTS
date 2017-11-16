from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from core.models import Organisation, Contact, Sector, Currency, Spreadsheet, Entry, Year, Recipient
from unicodecsv import writer as csvwriter
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import SpreadsheetForm
from .util import *
from django.db.models import Sum
from itertools import chain, groupby

@login_required
def edit(request,year):
    warnings = []
    user = request.user
    contact = get_object_or_404(Contact,user=user)
    organisation = contact.organisation
    recipients = Recipient.objects.all()
    statuses = Entry.PLEDGE_OR_DISB_CHOICES
    if not organisation.sectors.all():
        sectors = Sector.objects.filter(default=True)
    else:
        organisationSectors = organisation.sectors.all()
        defaultSectors = Sector.objects.filter(default=True)
        unionSectors = organisationSectors | defaultSectors
        sectors = unionSectors.distinct()
    years = Year.objects.all().order_by('value')
    year = int(year)
    if request.method == "POST":
        form = SpreadsheetForm(request.POST)
        queryDict = request.POST
        comment = queryDict.get('comment')
        if not Spreadsheet.objects.filter(organisation=organisation,year__value=year).exists():
            spreadsheet = form.save(commit=False)
            spreadsheet.year = Year.objects.get(value=year)
            spreadsheet.organisation = organisation
            spreadsheet.save()
        else:
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year__value=year)
            form = SpreadsheetForm(request.POST,instance=spreadsheet)
            spreadsheet = form.save()
        excludeKeys = ["currency","comment","agency","csrfmiddlewaretoken"]
        for key, value in queryDict.iteritems():
            if Entry.objects.filter(spreadsheet=spreadsheet,coordinates=key).exists():
                entry = Entry.objects.get(spreadsheet=spreadsheet,coordinates=key)
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save_reverse()
                else:
                    entry.delete()
            elif key not in excludeKeys and value!="":
                entry = Entry()
                entry.spreadsheet = spreadsheet
                entry.coordinates = key
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save_reverse()
        return redirect(spreadsheet)
    else:
        if Spreadsheet.objects.filter(organisation=organisation,year__value=year).exists():
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year__value=year)
            form = SpreadsheetForm(instance=spreadsheet)
            entries = Entry.objects.filter(spreadsheet=spreadsheet)
            currency = spreadsheet.currency
            spreadsheet_exists = True
            
            #Validate sums here
            #Grants table
            gt = entries.filter(spreadsheet=spreadsheet,sector__isnull=True)
            gt_sum = gt.values('recipient__single_letter_code').annotate(total = Sum('amount')).order_by('recipient__single_letter_code')
            gt_sum_obj = {this_sum['recipient__single_letter_code']:this_sum['total'] for this_sum in gt_sum} 
            #Sector grants
            sg = entries.filter(spreadsheet=spreadsheet,sector__isnull=False)
            sg_sum = sg.values('recipient__single_letter_code').annotate(total = Sum('amount')).order_by('recipient__single_letter_code')
            sg_sum_obj = {this_sum['recipient__single_letter_code']:this_sum['total'] for this_sum in sg_sum} 
            #Compare grants
            for recipient in recipients:
                code = recipient.single_letter_code
                total_grants = 0
                if code in gt_sum_obj:
                    total_grants = total_grants + gt_sum_obj[code]
                if code in sg_sum_obj:
                    grant_sectors = sg_sum_obj[code]
                    if total_grants>grant_sectors:
                        warnings.append("Warning: Total grants do not equal grants by sector for %s. Total grants are greater by %s" % (recipient.name,(total_grants-grant_sectors)))
                    if total_grants<grant_sectors:
                        warnings.append("Warning: Total grants do not equal grants by sector for %s. Grants by sector are greater by %s" % (recipient.name,(grant_sectors-total_grants)))
                        
        else:
            form = SpreadsheetForm()
            entries = []
            currency = []
            spreadsheet_exists = False
    return render(request,'core/edit-locked.html', {"warnings":warnings,"user":user,"contact":contact,"form":form,"entries":entries,"recipients":recipients,"statuses":statuses,"sectors":sectors,"years":years,"selected_year":year,"currency":currency,"spreadsheet_exists":spreadsheet_exists})

@login_required
def adminEdit(request,slug,year):
    warnings = []
    user = request.user
    if not user.is_staff:
        return redirect("core.views.edit",year=year)
    contact = get_object_or_404(Contact,user=user)
    organisation = Organisation.objects.get(slug=slug)
    recipients = Recipient.objects.all()
    statuses = Entry.PLEDGE_OR_DISB_CHOICES
    if not organisation.sectors.all():
        sectors = Sector.objects.filter(default=True)
    else:
        organisationSectors = organisation.sectors.all()
        defaultSectors = Sector.objects.filter(default=True)
        unionSectors = organisationSectors | defaultSectors
        sectors = unionSectors.distinct()
    years = Year.objects.all().order_by('value')
    year = int(year)
    if request.method == "POST":
        form = SpreadsheetForm(request.POST)
        queryDict = request.POST
        comment = queryDict.get('comment')
        if not Spreadsheet.objects.filter(organisation=organisation,year__value=year).exists():
            spreadsheet = form.save(commit=False)
            spreadsheet.year = Year.objects.get(value=year)
            spreadsheet.organisation = organisation
            spreadsheet.save()
        else:
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year__value=year)
            form = SpreadsheetForm(request.POST,instance=spreadsheet)
            spreadsheet = form.save()
        excludeKeys = ["currency","comment","agency","csrfmiddlewaretoken"]
        for key, value in queryDict.iteritems():
            if Entry.objects.filter(spreadsheet=spreadsheet,coordinates=key).exists():
                entry = Entry.objects.get(spreadsheet=spreadsheet,coordinates=key)
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save_reverse()
                else:
                    entry.delete()
            elif key not in excludeKeys and value!="":
                entry = Entry()
                entry.spreadsheet = spreadsheet
                entry.coordinates = key
                if safeFloat(value)>=0:
                    entry.amount = safeFloat(value)
                    entry.save_reverse()
        return redirect("core.views.adminEdit",slug=slug,year=year)
    else:
        if Spreadsheet.objects.filter(organisation=organisation,year__value=year).exists():
            spreadsheet = Spreadsheet.objects.get(organisation=organisation,year=year)
            form = SpreadsheetForm(instance=spreadsheet)
            entries = Entry.objects.filter(spreadsheet=spreadsheet)
            currency = spreadsheet.currency
            spreadsheet_exists = True
            #Validate sums here
            #Grants table
            gt = entries.filter(spreadsheet=spreadsheet,sector__isnull=True)
            gt_sum = gt.values('recipient__single_letter_code').annotate(total = Sum('amount')).order_by('recipient__single_letter_code')
            gt_sum_obj = {this_sum['recipient__single_letter_code']:this_sum['total'] for this_sum in gt_sum} 
            #Sector grants
            sg = entries.filter(spreadsheet=spreadsheet,sector__isnull=False)
            sg_sum = sg.values('recipient__single_letter_code').annotate(total = Sum('amount')).order_by('recipient__single_letter_code')
            sg_sum_obj = {this_sum['recipient__single_letter_code']:this_sum['total'] for this_sum in sg_sum} 
            #Compare grants
            for recipient in recipients:
                code = recipient.single_letter_code
                total_grants = 0
                if code in gt_sum_obj:
                    total_grants = total_grants + gt_sum_obj[code]
                if code in sg_sum_obj:
                    grant_sectors = sg_sum_obj[code]
                    if total_grants>grant_sectors:
                        warnings.append("Warning: Total grants do not equal grants by sector for %s. Total grants are greater by %s" % (recipient.name,(total_grants-grant_sectors)))
                    if total_grants<grant_sectors:
                        warnings.append("Warning: Total grants do not equal grants by sector for %s. Grants by sector are greater by %s" % (recipient.name,(grant_sectors-total_grants)))
    
        else:
            form = SpreadsheetForm()
            entries = []
            currency = []
            spreadsheet_exists = False
    return render(request,'core/edit.html', {"warnings":warnings,"user":user,"contact":contact,"organisation":organisation,"form":form,"entries":entries,"recipients":recipients,"statuses":statuses,"sectors":sectors,"years":years,"selected_year":year,"currency":currency,"spreadsheet_exists":spreadsheet_exists})

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
    writer = csvwriter(response,encoding='utf-8')
    header = ["Organisation","Agency","Status","Recipient","Sector","Year","Amount","Currency","Comment"]
    writer.writerow(header)
    for entry in entries:
        year = entry.spreadsheet.year.value
        comment = entry.spreadsheet.comment
        currency = entry.spreadsheet.currency
        agency = entry.spreadsheet.agency
        writer.writerow([organisation
                         ,agency
                         ,entry.pledge_or_disbursement_translate()
                         ,entry.recipient_translate()
                         ,entry.sector
                         ,year
                         ,entry.amount
                         ,currency
                         ,comment
                         ])
    return response

@login_required
def csv_all(request):
    user = request.user
    if user.is_staff:
        entries = Entry.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all.csv"'
        writer = csvwriter(response,encoding='utf-8')
        header = ["Organisation","Agency","Status","Recipient","Sector","Year","Amount","Currency","Comment"]
        writer.writerow(header)
        for entry in entries:
            organisation = entry.spreadsheet.organisation
            year = entry.spreadsheet.year.value
            agency = entry.spreadsheet.agency
            comment = entry.spreadsheet.comment
            currency = entry.spreadsheet.currency
            writer.writerow([organisation
                         ,agency
                         ,entry.pledge_or_disbursement_translate()
                         ,entry.recipient_translate()
                         ,entry.sector
                         ,year
                         ,entry.amount
                         ,currency
                         ,comment
                         ])
        return response
    else:
        return redirect(user.contact.organisation)

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