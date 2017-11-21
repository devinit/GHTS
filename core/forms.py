from django.forms import ModelForm
from core.models import Spreadsheet
from django.forms import SelectDateWidget
        
class SpreadsheetForm(ModelForm):
    class Meta:
        model = Spreadsheet
        fields = ('currency','comment','multisector_comment','othersector_comment','availability_date')
        widgets = {
            'availability_date':SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),)
        }