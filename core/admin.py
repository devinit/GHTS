from django.contrib import admin
from core.models import Contact, Organisation, Currency, Sector, Transaction, Spreadsheet, Entry
# Register your models here.

class ContactInline(admin.TabularInline):
    model = Contact

class OrganisationAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['name']
    inlines = [ContactInline,]
    prepopulated_fields = {'slug': ('name',), }
    #enable the save buttons on top of change form
    save_on_top = True
    
class CurrencyAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['iso','description','symbol']
    #enable the save buttons on top of change form
    save_on_top = True
    
class ContactAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['name','organisation']
    def name(self,obj):
        return obj.user.get_full_name()
    #enable the save buttons on top of change form
    save_on_top = True
    
class SectorAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ['name','loan_or_grant']
    #enable the save buttons on top of change form
    save_on_top = True
    
class TransactionAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ["transaction_number","organisation"
                    ,"loan_or_grant"
                    ,"concessional","pledge_or_disbursement"
                    ,"recipient","sector","channel_of_delivery","year","currency","amount"
                    ]
    list_filter = ["organisation"
                    ,"loan_or_grant"
                    ,"concessional","pledge_or_disbursement"
                    ,"recipient","sector","channel_of_delivery","year","currency","amount"
                    ]
    def transaction_number(self,obj):
        return obj.pk
    #enable the save buttons on top of change form
    save_on_top = True
    
class SpreadsheetAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ["year","organisation","currency"]
    list_filter = ["year","organisation","currency"]
    #enable the save buttons on top of change form
    save_on_top = True
    
class EntryAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ["spreadsheet","coordinates","amount"]
    list_filter = ["spreadsheet","coordinates","amount"]
    #enable the save buttons on top of change form
    save_on_top = True
    
admin.site.register(Organisation,OrganisationAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Sector,SectorAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Spreadsheet,SpreadsheetAdmin)
admin.site.register(Entry,EntryAdmin)