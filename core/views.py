from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from core.models import Organisation, Transaction
from csv import writer as csvwriter

def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

def csv(request,slug):
    organisation = get_object_or_404(Organisation,slug=slug)
    transactions = Transaction.objects.filter(organisation=organisation)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+slug+'.csv"'
    writer = csvwriter(response)
    header = ["Organisation","Humanitarian or development","Loan or grant","Concessional","Pledge or disbursement"
              ,"Recipient","Channel of delivery","Sector","Year","Amount","Currency"
              ,"Refugee facility for Turkey","Outside London Conference"]
    writer.writerow(header)
    for transaction in transactions:
        writer.writerow([transaction.organisation
                         ,transaction.hum_or_dev_verbose()
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
                         ,transaction.outside_london_conference])
    return response