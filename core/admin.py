from django.contrib import admin
from core.models import Contact, Organisation, Currency, Sector, Transaction
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
    list_display = ['name']
    #enable the save buttons on top of change form
    save_on_top = True
    
class TransactionAdmin(admin.ModelAdmin):
    #fields display on change list
    list_display = ["transaction_number","organisation"
                    ,"humanitarian_or_development","loan_or_grant"
                    ,"concessional","pledge_or_disbursement"
                    ,"recipient","sectors","year","currency","amount"
                    ]
    list_filter = ["organisation"
                    ,"humanitarian_or_development","loan_or_grant"
                    ,"concessional","pledge_or_disbursement"
                    ,"recipient","year","currency","amount"
                    ]
    filter_horizontal = ["sector"]
    def transaction_number(self,obj):
        return obj.pk
    def sectors(self, obj):
        return "; ".join([str(s) for s in obj.sector.all()])
    sectors.admin_order_field = 'sector'
    #enable the save buttons on top of change form
    save_on_top = True
    
admin.site.register(Organisation,OrganisationAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Sector,SectorAdmin)
admin.site.register(Transaction,TransactionAdmin)