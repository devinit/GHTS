from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Currency(models.Model):
    symbol = models.CharField(max_length=1)
    iso = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['iso']
        verbose_name_plural = "currencies"
    
    def __str__(self):
        return self.iso

class Organisation(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse("core.views.csv",args=[self.slug])

class Contact(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    organisation = models.ForeignKey(Organisation)
    
    def __str__(self):
        return self.user.get_full_name()
    
    def __unicode__(self):
        return u'%s' % self.user.get_full_name()
    
class Sector(models.Model):
    name = models.CharField(max_length=255)
    LOAN_OR_GRANT_CHOICES = (
        ('L','Loan'),
        ('G','Grant'),
    )
    loan_or_grant = models.CharField(max_length=1,choices=LOAN_OR_GRANT_CHOICES,default='G')
    def loan_verbose(self):
        return dict(Transaction.LOAN_OR_GRANT_CHOICES)[self.loan_or_grant]
    
    def __unicode__(self):
        return u'%s' % self.name

    
class Transaction(models.Model):
    organisation = models.ForeignKey(Organisation)
    LOAN_OR_GRANT_CHOICES = (
        ('','---------'),
        ('L','Loan'),
        ('G','Grant'),
    )
    loan_or_grant = models.CharField(max_length=1,choices=LOAN_OR_GRANT_CHOICES,blank=True,null=True)
    def loan_verbose(self):
        return dict(Transaction.LOAN_OR_GRANT_CHOICES)[self.loan_or_grant]
    concessional = models.BooleanField(default=True)
    PLEDGE_OR_DISB_CHOICES = (
        ('','---------'),
        ('P','Pledged'),
        ('M','Committed'),
        ('C','Contracted'),
        ('D','Disbursed'),
    )
    pledge_or_disbursement = models.CharField(max_length=1,choices=PLEDGE_OR_DISB_CHOICES,blank=True,null=True)
    def pledge_or_disb_verbose(self):
        return dict(Transaction.PLEDGE_OR_DISB_CHOICES)[self.pledge_or_disbursement]
    RECIPIENT_CHOICES = (
        ('S','Syria'),
        ('J','Jordan'),
        ('L','Lebanon'),
        ('I','Iraq'),
        ('E','Egypt'),
        ('T','Turkey'),
        ('R','Region'),
        ('N','Not defined'),
    )
    recipient = models.CharField(max_length=1,choices=RECIPIENT_CHOICES,default="N")
    def recipient_verbose(self):
        return dict(Transaction.RECIPIENT_CHOICES)[self.recipient]
    DELIVERY_CHOICES = (
        ('','---------'),
        ('U','UN agencies'),
        ('N','NGOs'),
        ('R','RCRC'),
        ('G','Government institutions'),
        ('P','Private sector'),
        ('O','Other channel of delivery'),
    )
    channel_of_delivery = models.CharField(max_length=1,choices=DELIVERY_CHOICES,blank=True,null=True)
    def delivery_verbose(self):
        return dict(Transaction.DELIVERY_CHOICES)[self.channel_of_delivery]
    sector = models.ForeignKey(Sector,blank=True,null=True)
    YEAR_CHOICES = (
        (2016,2016),
        (2017,2017),
        (2018,2018),
        (2019,2019),
        (2020,2020),
    )
    year = models.IntegerField(choices=YEAR_CHOICES,blank=True,null=True)
    amount = models.DecimalField(max_digits=99, decimal_places=2,blank=True,null=True,help_text="If no amount was pledged/disbursed, record amount as zero. Otherwise leave field missing for unknown amount.")
    currency = models.ForeignKey(Currency,blank=True,null=True)
    refugee_facility_for_turkey = models.BooleanField(default=False,help_text="Was/is the above amount meant for the Refugee Facility for Turkey?")
    comment = models.TextField(null=True,blank=True)
    
class Spreadsheet(models.Model):
    YEAR_CHOICES = (
        (2016,2016),
        (2017,2017),
        (2018,2018),
        (2019,2019),
        (2020,2020),
    )
    year = models.IntegerField(choices=YEAR_CHOICES)
    currency = models.ForeignKey(Currency)
    organisation = models.ForeignKey(Organisation)
    
class Entry(models.Model):
    coordinates = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=99, decimal_places=2,blank=True,null=True)
    spreadsheet = models.ForeignKey(Spreadsheet)


