from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    iso = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['iso']
        verbose_name_plural = "currencies"
    
    def __str__(self):
        return self.iso
    
class Sector(models.Model):
    name = models.CharField(max_length=255,unique=True)
    default = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def save(self, *args, **kwargs):
        super(Sector, self).save(*args, **kwargs)
        if self.name:
            self.name = self.name.replace('"',"'")
        super(Sector, self).save(*args, **kwargs)

class Organisation(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    sectors = models.ManyToManyField(Sector,related_name="sectors",related_query_name="sector",blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse("core.views.adminEdit",args=[self.slug,2016])
    
    def get_export_url(self):
        return reverse("core.views.csv",args=[self.slug])

class Contact(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    organisation = models.ForeignKey(Organisation)
    
    def __str__(self):
        return self.user.get_full_name()
    
    def __unicode__(self):
        return u'%s' % self.user.get_full_name()
    
    
class Year(models.Model):
    value = models.IntegerField(unique=True)
    
    def __str__(self):
        return str(self.value)
    
    def __unicode__(self):
        return u'%s' % self.value
    
class Spreadsheet(models.Model):
    year = models.ForeignKey(Year)
    agency = models.CharField(max_length=255,null=True,blank=True)
    currency = models.ForeignKey(Currency)
    organisation = models.ForeignKey(Organisation)
    comment = models.TextField(null=True,blank=True)
    
    def get_absolute_url(self):
        return reverse("core.views.edit",args=[self.year.value])
    
class Entry(models.Model):
    coordinates = models.CharField(max_length=300,editable=False)
    amount = models.DecimalField(max_digits=99, decimal_places=2,blank=True,null=True)
    spreadsheet = models.ForeignKey(Spreadsheet,editable=False)
    PLEDGE_OR_DISB_CHOICES = (
        ('O','Overall programming')
        ,('T','Transfers to beneficiaries')
        ,('C','Cash')
        ,('V','Voucher')
        ,('N','Conditional')
        ,('U','Unconditional')
    )
    RECIPIENT_CHOICES = (
        ('G','Germany'),
        ('S','Sweden'),
        ('N','Norway'),
        ('U','United Kingdom')
    )
    pledge_or_disbursement = models.CharField(max_length=1,choices=PLEDGE_OR_DISB_CHOICES,blank=True,null=True)
    recipient = models.CharField(max_length=1,choices=RECIPIENT_CHOICES,default="N")
    sector = models.ForeignKey(Sector,blank=True,null=True)
    def pledge_or_disbursement_lookup(self):
        val = self.coordinates.split("|")[0]
        return val
    def recipient_lookup(self):
        val = self.coordinates.split("|")[1]
        return val
    def sector_lookup(self):
        val = self.coordinates.split("|")[2]
        return val
    def pledge_or_disbursement_translate(self):
        val = self.coordinates.split("|")[0]
        if val is None or val=="":
            return ""
        else:
            return dict(Entry.PLEDGE_OR_DISB_CHOICES)[val]
    def recipient_translate(self):
        val = self.coordinates.split("|")[1]
        if val is None or val=="":
            return ""
        else:
            return dict(Entry.RECIPIENT_CHOICES)[val]
    def sector_translate(self):
        val = self.coordinates.split("|")[2]
        return val

    class Meta:
        verbose_name_plural = "entries"
        
    def save(self, *args, **kwargs):
        #Coordinates are pledge|recip|sector
        coord_list = [
            self.pledge_or_disbursement if self.pledge_or_disbursement else ""
            ,self.recipient if self.recipient else ""
            ,self.sector if self.sector else ""
        ]
        self.coordinates = "|".join(coord_list)
        super(Entry, self).save(*args, **kwargs)
        
    def save_reverse(self, *args, **kwargs):
        self.pledge_or_disbursement =  self.pledge_or_disbursement_lookup()
        self.recipient = self.recipient_lookup()
        if Sector.objects.filter(name=self.sector_lookup()).exists():
            self.sector = Sector.objects.get(name=self.sector_lookup())
        super(Entry, self).save(*args, **kwargs)


