from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from core.models import Organisation, Transaction, Contact
from csv import writer as csvwriter
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm

@login_required
def add(request):
    user = request.user
    contact = get_object_or_404(Contact,user=user)
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.organisation = contact.organisation
            transaction.save()
            return redirect('admin:core_transaction_changelist')
    else:
        form = TransactionForm()
    return render(request,'core/add.html', {"user":user,"contact":contact,"form":form})

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