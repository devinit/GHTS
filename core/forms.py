from django.forms import ModelForm
from core.models import Spreadsheet
        
class SpreadsheetForm(ModelForm):
    class Meta:
        model = Spreadsheet
        fields = ('currency','agency','comment','multisector_comment','availability_date')